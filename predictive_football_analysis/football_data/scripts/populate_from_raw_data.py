import csv

from football_data.models import League, Team, Stadium
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
                            season=season)
                        )

                    team_name = team_names_map.match_team_by_league(row[2], league_teams)
                    if Team.objects.filter(name=team_name).count() == 0:
                        Team.objects.create(name=team_name, league=league)


def import_stadiums():
    file_path = 'football_data/raw_data/jokecamp-footballdata/stadiums-with-GPS-coordinates.csv'

    with open(file_path, 'r') as stadium_file:
        reader = csv.reader(stadium_file)

        # Skip headers line
        next(reader)

        for row in reader:
            try:
                team_name = team_names_map.match_team_name(row[1])
            except Exception:
                continue

            if Team.objects.filter(name=team_name).count() == 1:
                team = Team.objects.get(name=team_name)

                Stadium.objects.create(
                    name=row[3],
                    lat=row[5],
                    lng=row[6],
                    team=team,
                )


def run():
    create_leagues()
    import_teams()
    import_stadiums()
