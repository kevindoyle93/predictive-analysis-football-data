import csv
import datetime

from football_data.models import League, Team, Match
from football_data.raw_data import team_names_map


def create_leagues():
    League.objects.all().delete()

    League.objects.create(name='Premier League', country='GB')
    League.objects.create(name='La Liga', country='ES')
    League.objects.create(name='Ligue Un', country='FR')
    League.objects.create(name='Serie A', country='IT')
    League.objects.create(name='Bundesliga', country='DE')

    if League.objects.count() != 5:
        raise Exception('Looks like the teams didn\'t load, what\'s up with that?')
    else:
        print('Leagues done!')


def import_teams():
    Team.objects.all().delete()

    kaggle_teams = {}
    # Get team names and API IDs from the Kaggle dataset
    with open('football_data/raw_data/kaggle-data/Team.csv', 'r') as kaggle_team_file:
        reader = csv.reader(kaggle_team_file)

        # Skip headers line
        next(reader)
        for row in reader:
            team_name = team_names_map.match_team_name(row[3])
            kaggle_teams[team_name] = int(row[2])

    file_path = 'football_data/raw_data/football-data-co-uk/'
    leagues = [
        ('premier_league/', 'Premier League', team_names_map.PREMIER_LEAGUE),
        ('bundesliga/', 'Bundesliga', team_names_map.BUNDESLIGA),
        ('la_liga/', 'La Liga', team_names_map.LA_LIGA),
        ('ligue_un/', 'Ligue Un', team_names_map.LIGUE_UN),
        ('serie_a/', 'Serie A', team_names_map.SERIE_A),
    ]

    seasons = [
        '2011-2012.csv',
        '2012-2013.csv',
        '2013-2014.csv',
        '2014-2015.csv',
        '2015-2016.csv',
        '2016-2017.csv',
    ]

    for league_name in leagues:
        league_path = league_name[0]
        league = League.objects.get(name=league_name[1])
        league_teams = league_name[2]

        for season in seasons:
            with open(file_path + league_path + season, 'r') as match_file:
                reader = csv.reader(match_file)

                # Skip headers line
                next(reader)

                for row in reader:
                    if row[2] == '':
                        raise Exception('Missing value for {league} - {season}'.format(
                            league=league.name,
                            season=season,)
                        )

                    team_name = team_names_map.match_team_by_league(row[2], league_teams)
                    if Team.objects.filter(name=team_name).count() == 0:
                        Team.objects.create(
                            name=team_name,
                            league=league,
                        )


def import_matches():
    Match.objects.all().delete()
    file_path = 'football_data/raw_data/football-data-co-uk/'
    leagues = [
        ('premier_league/', team_names_map.PREMIER_LEAGUE),
        ('bundesliga/', team_names_map.BUNDESLIGA),
        ('la_liga/', team_names_map.LA_LIGA),
        ('ligue_un/', team_names_map.LIGUE_UN),
        ('serie_a/', team_names_map.SERIE_A),
    ]

    seasons = [
        '2011-2012.csv',
        '2012-2013.csv',
        '2013-2014.csv',
        '2014-2015.csv',
        '2015-2016.csv',
        '2016-2017.csv',
    ]

    for league_name in leagues:
        print(league_name[0])
        league_path = league_name[0]
        league_teams = league_name[1]

        stats_index = 11 if league_name == leagues[0] else 10

        for season in seasons:
            with open(file_path + league_path + season, 'r') as match_file:
                reader = csv.reader(match_file)

                # Skip headers line
                next(reader)
                for row in reader:
                    home_team = Team.objects.get(name=team_names_map.match_team_by_league(row[2], league_teams))
                    away_team = Team.objects.get(name=team_names_map.match_team_by_league(row[3], league_teams))
                    try:
                        Match.objects.create(
                            date=datetime.datetime.strptime(row[1], '%d/%m/%y'),
                            home_team=home_team,
                            away_team=away_team,
                            full_time_home_goals=row[4],
                            full_time_away_goals=row[5],
                            full_time_result=row[6],
                            half_time_home_goals=row[7],
                            half_time_away_goals=row[8],
                            half_time_result=row[9],
                            home_total_shots=row[stats_index],
                            away_total_shots=row[stats_index + 1],
                            home_shots_on_target=row[stats_index + 2],
                            away_shots_on_target=row[stats_index + 3],
                            home_fouls_committed=row[stats_index + 4],
                            away_fouls_committed=row[stats_index + 5],
                            home_corners=row[stats_index + 6],
                            away_corners=row[stats_index + 7],
                            home_yellow_cards=row[stats_index + 8],
                            away_yellow_cards=row[stats_index + 9],
                            home_red_cards=row[stats_index + 10],
                            away_red_cards=row[stats_index + 11],
                        )
                    except Exception:
                        print('{h} v {a} {d}'.format(h=home_team.name, a=away_team.name, d=row[1]))
                        return


def run():
    print('Creating leagues...')
    create_leagues()
    print('Importing teams...')
    import_teams()
    print('Importing matches...')
    import_matches()
