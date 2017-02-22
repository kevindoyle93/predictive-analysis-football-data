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
    'Manchester United': ['Man United', 'Man Utd'],
    'Middlesbrough': ['Middlesbrough', 'Middlesbrogh', 'M\'boro'],
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
    'West Bromwich Albion': ['West Brom', 'West Bromich Albion', 'W Brom'],
    'Wigan Athletic': ['Wigan'],
    'Wolverhampton Wanderers': ['Wolves'],
}

BUNDESLIGA = {
    'Augsburg': ['FC Augsburg'],
    'Bayer Leverkusen': ['Leverkusen'],
    'Bayern Munich': [],
    'Borussia Dortmund': ['Dortmund', 'B Dortmund'],
    'Borussia Monchengladbach': ['M\'gladbach', 'Borussia Moenchengladbach'],
    'Darmstadt 98': ['Darmstadt', 'SV Darmstadt 98'],
    'Eintracht Braunschweig': ['Braunschweig', 'E Braunschweig'],
    'Eintracht Frankfurt': ['Ein Frankfurt', 'Frankfurt'],
    'FC Koln': ['FC Cologne', 'Cologne'],
    'Fortuna Dusseldorf': ['Fortuna Duesseldorf', 'F Dusseldorf'],
    'Freiburg': ['SC Freiburg'],
    'Greuther Furth': ['Greuther Fuerth'],
    'Hamburg': ['Hamburger SV'],
    'Hannover 96': ['Hannover'],
    'Hertha Berlin': ['Hertha'],
    'Hoffenheim': [],
    'Ingolstadt': ['FC Ingolstadt 04'],
    'Kaiserslautern': [],
    'Mainz 05': ['Mainz'],
    'Nurnberg': ['Nuernberg', 'FC Nurnberg'],
    'Paderborn 07': ['Paderborn', 'SC Paderborn 07'],
    'Red Bull Leipzig': ['RB Leipzig'],
    'Schalke 04': ['Shalke', 'Schalke'],
    'Stuttgart': ['VfB Stuttgart'],
    'Werder Bremen': [],
    'Wolfsburg': [],
}

LA_LIGA = {
    'Almeria': [],
    'Athletic Bilbao': ['Ath Bilbao'],
    'Atletico Madrid': ['Ath Madrid'],
    'Barcelona': [],
    'Celta Vigo': ['Celta'],
    'Cordoba': [],
    'Deportivo Alaves': ['Alaves'],
    'Deportivo La Coruna': ['La Coruna', 'Deportivo'],
    'Eibar': [],
    'Elche': [],
    'Espanyol': ['Espanol'],
    'Getafe': [],
    'Granada': [],
    'Las Palmas': [],
    'Leganes': ['CD Leganes'],
    'Levante': [],
    'Malaga': [],
    'Mallorca': ['Real Mallorca'],
    'Osasuna': [],
    'Racing Santander': ['Santander'],
    'Rayo Vallecano': ['Vallecano'],
    'Real Betis': ['Betis'],
    'Real Madrid': [],
    'Real Sociedad': ['Sociedad'],
    'Sevilla': [],
    'Sporting Gijon': ['Sp Gijon'],
    'Valencia': [],
    'Valladolid': ['Real Valladolid'],
    'Villarreal': [],
    'Zaragoza': ['Real Zaragoza'],
}

LIGUE_UN = {
    'AC Ajaccio': ['Ajaccio'],
    'Angers': [],
    'Auxerre': [],
    'Bastia': ['SC Bastia'],
    'Bordeaux': [],
    'Brest': [],
    'Caen': [],
    'Dijon': [],
    'Evian': ['Evian Thonon Gaillard'],
    'Gazelec Ajaccio': ['Ajaccio GFCO', 'GFC Ajaccio'],
    'Guingamp': [],
    'Lens': ['RC Lens'],
    'Lille': [],
    'Lorient': [],
    'Lyon': [],
    'Marseille': [],
    'Metz': [],
    'Monaco': [],
    'Montpellier': [],
    'Nancy': [],
    'Nantes': [],
    'Nice': [],
    'Paris Saint-Germain': ['Paris SG', 'Paris Saint Germain', 'PSG'],
    'Reims': [],
    'Rennes': [],
    'Saint-Etienne': ['St Etienne'],
    'Sochaux': [],
    'Toulouse': [],
    'Troyes': [],
    'Valenciennes': [],
}

SERIE_A = {
    'Atalanta': [],
    'Bologna': [],
    'Cagliari': [],
    'Carpi': [],
    'Catania': [],
    'Cesena': [],
    'Chievo': [],
    'Crotone': ['FC Crotone'],
    'Empoli': [],
    'Fiorentina': [],
    'Frosinone': [],
    'Genoa': [],
    'Hellas Verona': ['Verona'],
    'Inter': ['Inter Milan'],
    'Juventus': [],
    'Lazio': [],
    'Lecce': [],
    'Livorno': [],
    'Milan': ['AC Milan'],
    'Napoli': ['SSC Napoli'],
    'Novara': [],
    'Palermo': [],
    'Parma': [],
    'Pescara': [],
    'Roma': [],
    'Sampdoria': [],
    'Sassuolo': [],
    'Siena': ['Robur Siena'],
    'Torino': [],
    'Udinese': [],
}


def match_team_name(team):
    for league in [PREMIER_LEAGUE, BUNDESLIGA, LA_LIGA, LIGUE_UN, SERIE_A]:
        for correct_name, possible_names in league.items():
            if team == correct_name or team in possible_names:
                return correct_name

    raise Exception('No match found for team: {team}'.format(team=team))


def match_team_by_league(team, league):
    for correct_name, possible_names in league.items():
        if team == correct_name or team in possible_names:
            return correct_name

    raise Exception('No match found for team: {team}'.format(team=team))
