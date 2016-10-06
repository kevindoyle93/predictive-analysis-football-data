from football_data.models import League

DATA_FOLDER = '../raw_data/'


def create_leagues():
    League.objects.create(name='Premier League', country='GB')
    League.objects.create(name='La Liga', country='ES')
    League.objects.create(name='Ligue Un', country='FR')
    League.objects.create(name='Serie A', country='IT')
    League.objects.create(name='Bundesliga', country='DE')

    if League.objects.count() != 5:
        raise Exception('Looks like the teams didn\'t load, what\'s up with that?')


def run():
    create_leagues()
