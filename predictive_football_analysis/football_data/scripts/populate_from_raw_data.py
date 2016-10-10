import csv
import datetime

from football_data.models import League, Team, Stadium, Player, Match
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
                            kaggle_api_id=kaggle_teams[team_name]
                        )


def import_stadiums():
    Stadium.objects.all().delete()
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
                    capacity=row[4],
                )


def import_players():
    Player.objects.all().delete()
    file_path = 'football_data/raw_data/kaggle-data/Player.csv'
    dob_format = '%Y-%m-%d'
    with open(file_path, 'r') as player_file:
        reader = csv.reader(player_file)

        # Skip headers line
        next(reader)

        for row in reader:
            dob_string = row[5][:10]
            dob = datetime.datetime.strptime(dob_string, dob_format).date()
            Player.objects.create(
                name=row[3],
                kaggle_api_id=row[2],
                date_of_birth=dob,
                height=row[6],
                weight=row[7]
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


def import_lineups():
    file_paths = ['football_data/raw_data/kaggle-data/Match_1.csv', 'football_data/raw_data/kaggle-data/Match_2.csv']

    for file_path in file_paths:
        with open(file_path, 'r') as match_file:
            reader = csv.reader(match_file)

            # Skip headers line
            next(reader)

            for row in reader:
                read_lineups(row)


def read_lineups(row):
    home_player_index = 56
    away_player_index = home_player_index + 11
    home_player_pos_index = 34
    away_player_pos_index = home_player_pos_index + 11
    try:
        home_team = Team.objects.get(kaggle_api_id=row[8])
    except Team.DoesNotExist:
        return
    away_team = Team.objects.get(kaggle_api_id=row[9])
    date = datetime.datetime.strptime(row[6], '%d/%m/%Y %H:%M')

    try:
        match = Match.objects.get(date=date, home_team=home_team, away_team=away_team)
    except Match.DoesNotExist:
        raise Exception('{h} v {a} {d} does not exist'.format(
            h=home_team,
            a=away_team,
            d=date,
        ))
    for num in range(0, 11):
        try:
            home_player = Player.objects.get(kaggle_api_id=row[home_player_index + num])
            setattr(match, 'home_player_{n}'.format(n=num + 1), home_player)
            home_player.has_played_match = True
            home_player.save()
        except ValueError:
            pass
        try:
            away_player = Player.objects.get(kaggle_api_id=row[away_player_index + num])
            setattr(match, 'away_player_{n}'.format(n=num + 1), away_player)
            away_player.has_played_match = True
            away_player.save()
        except ValueError:
            pass
        setattr(match, 'home_player_{n}_pos'.format(n=num + 1), row[home_player_pos_index + num])
        setattr(match, 'away_player_{n}_pos'.format(n=num + 1), row[away_player_pos_index + num])
        match.save()


def remove_excess_players():
    """
    The Player.csv dataset contains players from before my scope and from leagues outside my scope that must be removed
    """
    Player.objects.filter(has_played_match=False).all().delete()


def run():
    print('Creating leagues...')
    create_leagues()
    print('Importing teams...')
    import_teams()
    print('Importing stadiums...')
    import_stadiums()
    print('Importing players...')
    import_players()
    print('Importing matches...')
    import_matches()
    print('Importing lineups...')
    import_lineups()
    print('Removing excess players...')
    remove_excess_players()
