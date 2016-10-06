from lxml import html
import requests
import json
import re

import team_names_map

BASE_URL = 'http://www.sportinglife.com'
YEARS = [
	'2011',
	'2012',
	'2013',
	'2014',
	'2015',
	'2016',
]
MONTHS = [
	'january',
	'february',
	'march',
	'april',
	'may',
	'august',
	'september',
	'october',
	'november',
	'december',
]


sport = '/football/'
league = 'premier-league/'
results_page = 'results/'
month = 'may-2015'

page = requests.get(BASE_URL + sport + league + results_page + month)
root = html.fromstring(page.content)

team_names = []
for container in root.xpath('//*[@class="ixx"]'):
	team_names.append(container[0][0].text_content())

match_links = []
for match in root.xpath('//*[@class="ixxa"]'):
	link = re.sub('commentary', 'stats', match.get('href'))
	match_links.append(link)

match_count = 0;
for link in match_links:
	stats_page = html.fromstring(requests.get(BASE_URL + link).content)
	stats_lists = stats_page.xpath('//*[@class="s-con"]')

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

	home_possession = float(home_possession_str.split('%')[1][1:])
	away_possession = float(away_possession_str.split('%')[1][1:])
	print('{ht} {hp} - {ap} {at}'.format(
			ht=home_team,
			hp=home_possession, 
			ap=away_possession,
			at=away_team
		)
	)

	match_count += 1
