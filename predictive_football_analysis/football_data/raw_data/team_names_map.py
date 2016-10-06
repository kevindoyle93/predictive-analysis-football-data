PREMIER_LEAGUE = [
    'Arsenal',
    'Aston Villa',
    'Blackburn Rovers',
    'Bolton Wanderers',
    'Bournemouth',
    'Burnley',
    'Cardiff City',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Hull City',
    'Leicester City',
    'Liverpool',
    'Manchester City',
    'Manchester United',
    'Newcastle United',
    'Norwich City',
    'Queens Park Rangers',
    'Reading',
    'Southampton',
    'Stoke City',
    'Sunderland',
    'Swansea City',
    'Tottenham Hotspur',
    'Watford',
    'West Ham United',
    'West Bromich Albion',
    'Wigan Athletic',
    'Wolverhampton Wanderers',
]


def match_team_name(team):
    for team_name in PREMIER_LEAGUE:
        if all((c in team_name.lower()) for c in team.lower()):
            return team_name
