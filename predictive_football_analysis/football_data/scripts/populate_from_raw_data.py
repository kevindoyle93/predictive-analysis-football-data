import csv

from football_data.models import League, Team
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


def import_teams():
    Team.objects.all().delete()

    file_path = 'football_data/raw_data/football-data-co-uk/premier_league/'
    seasons = [
        '2011-2012.csv',
        '2012-2013.csv',
        '2013-2014.csv',
        '2014-2015.csv',
        '2015-2016.csv',
    ]

    league = League.objects.get(name='Premier League')

    for season in seasons:
        with open(file_path + season, 'r') as match_file:
            reader = csv.reader(match_file)

            # Skip headers line
            next(reader)

            for row in reader:
                team_name = team_names_map.match_team_name(row[2])
                if Team.objects.filter(name=team_name).count() == 0:
                    Team.objects.create(name=team_name, league=league)


def run():
    create_leagues()
    import_teams()
