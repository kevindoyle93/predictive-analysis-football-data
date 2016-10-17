from lxml import html
import requests
import re
import time

from football_data.raw_data import team_names_map
from football_data.models import Match, Team

BASE_URL = 'http://www.sportinglife.com/'

YEARS = [
    # '2011',
    # '2012',
    # '2013',
    # '2014',
    # '2015',
    '2016',
]

MONTHS = {
    # 'january',
    # 'february',
    # 'march',
    # 'april',
    'may': 5,
    # 'august',
    # 'september',
    # 'october',
    # 'november',
    # 'december',
}

LEAGUES = [
    'premier-league',
]


def get_results_url(league, date):
    return '{base}/football/{league}/results/{date}'.format(base=BASE_URL, league=league, date=date)


def format_date(month, year):
    return '{month}-{year}'.format(month=month, year=year)


def get_results_page_root(url):
    page = requests.get(url)
    return html.fromstring(page.content)


def fetch_possession_stats():
    for league in LEAGUES:
        for year in YEARS:
            for month, month_index in MONTHS.items():
                url = get_results_url(league, format_date(month, year))
                root = get_results_page_root(url)

                # Get the teams
                team_names = []
                for container in root.xpath('//*[@class="ixx"]'):
                    team_names.append(container[0][0].text_content())

                # Get the links to the stats pages of each match
                match_links = []
                for match in root.xpath('//*[@class="ixxa"]'):
                    link = re.sub('commentary', 'stats', match.get('href'))
                    match_links.append(link)

                match_count = 0
                for link in match_links:
                    stats_page = html.fromstring(requests.get(BASE_URL + link).content)
                    stats_lists = stats_page.xpath('//*[@class="s-con"]')

                    home_possession_str = None
                    away_possession_str = None

                    for stat in stats_lists[0]:
                        if isinstance(stat, html.HtmlComment):
                            continue
                        if 'Possession' in stat.text_content():
                            home_possession_str = stat.text_content()

                    for stat in stats_lists[1]:
                        if isinstance(stat, html.HtmlComment):
                            continue
                        if 'Possession' in stat.text_content():
                            away_possession_str = stat.text_content()

                    home_team = team_names_map.match_team_name(
                        team_names[match_count * 2]
                    )

                    away_team = team_names_map.match_team_name(
                        team_names[match_count * 2 + 1]
                    )

                    match_to_update = Match.objects.get(
                        home_team=Team.objects.get(name=home_team),
                        away_team=Team.objects.get(name=away_team),
                        date__year=int(year),
                        date__month=month_index,
                    )

                    home_possession = float(home_possession_str.split('%')[1][1:])
                    away_possession = float(away_possession_str.split('%')[1][1:])
                    print('{ht} {hp} - {ap} {at}'.format(
                            ht=home_team,
                            hp=home_possession,
                            ap=away_possession,
                            at=away_team,
                        )
                    )

                    match_to_update.home_possession = home_possession
                    match_to_update.away_possession = away_possession
                    match_to_update.save()

                    match_count += 1

                    # Wait before continuing, I don't want to overload sportinglife's servers
                    time.sleep(5)


fetch_possession_stats()
