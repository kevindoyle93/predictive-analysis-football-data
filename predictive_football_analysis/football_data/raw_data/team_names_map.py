PREMIER_LEAGUE = {
    'Arsenal': [],
    'Aston Villa': [],
    'Blackburn Rovers': ['Blackburn'],
    'Bolton Wanderers': ['Bolton'],
    'Bournemouth': [],
    'Burnley': [],
    'Cardiff City': ['Cardiff'],
    'Chelsea': [],
    'Crystal Palace': [],
    'Everton': [],
    'Fulham': [],
    'Hull City': ['Hull'],
    'Leicester City': ['Leicester'],
    'Liverpool': [],
    'Manchester City': ['Man City'],
    'Manchester United': ['Man United'],
    'Newcastle United': ['Newcastle'],
    'Norwich City': ['Norwich'],
    'Queens Park Rangers': ['QPR'],
    'Reading': [],
    'Southampton': [],
    'Stoke City': ['Stoke'],
    'Sunderland': [],
    'Swansea City': ['Swansea'],
    'Tottenham Hotspur': ['Tottenham'],
    'Watford': [],
    'West Ham United': ['West Ham'],
    'West Bromich Albion': ['West Brom'],
    'Wigan Athletic': ['Wigan'],
    'Wolverhampton Wanderers': ['Wolves'],
}

BUNDESLIGA = {
    'Augsburg': [],
    'Bayer Leverkusen': ['Leverkusen'],
    'Bayern Munich': [],
    'Borussia Dortmund': ['Dortmund'],
    'Borussia Monchengladbach': ['M\'gladbach'],
    'Darmstadt 98': ['Darmstadt'],
    'Eintracht Braunschweig': ['Braunschweig'],
    'Eintracht Frankfurt': ['Ein Frankfurt'],
    'FC Koln': [''],
    'Fortuna Dusseldorf': [],
    'Freiburg': [],
    'Greuther Furth': [],
    'Hamburg': [],
    'Hannover 96': ['Hannover'],
    'Hertha Berlin': ['Hertha'],
    'Hoffenheim': [],
    'Ingolstadt': [],
    'Kaiserslautern': [],
    'Mainz 05': ['Mainz'],
    'Nurnberg': [],
    'Paderborn 07': ['Paderborn'],
    'Schalke 04': [],
    'Stuttgart': [],
    'Werder Bremen': [],
    'Wolfsburg': [],
}


def match_team_name(team):
    for team_name in PREMIER_LEAGUE:
        if all((c in team_name.lower()) for c in team.lower()):
            return team_name


def match_team_by_league(team, league):
    for correct_name, possible_names in league.items():
        if team == correct_name or team in possible_names:
            return correct_name

    raise Exception('No match found for team: {team}'.format(team=team))
