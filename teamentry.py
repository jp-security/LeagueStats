from app import models, db

teams = [
{'team_owner': 'Darklord Destro',   'team_city': 'Washington',      'team_name': 'All Time Redskins',   'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'tjspeaks',          'team_city': 'Baltimore',       'team_name': 'All Time Ravens',     'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Aquick Assasin',    'team_city': 'Cleveland',       'team_name': 'Browns',              'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'MightyRx',          'team_city': 'Arizona',         'team_name': '2011 Cardinals',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'RebelRouser1988',   'team_city': 'Tampa Bay',       'team_name': '1984 Buccanneers',    'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Dazzo47',           'team_city': 'Chicago',         'team_name': 'All Time Bears',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'SitnHereFlossin',   'team_city': 'Carolina',        'team_name': '2015 Panthers',       'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Pcat Magoo',        'team_city': 'Kansas City',     'team_name': 'All Time Chiefs',     'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'xRun and Sh00tx',   'team_city': 'Houston',         'team_name': 'Oilers',              'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'HeavyHitter55',     'team_city': 'Philadelphia',    'team_name': 'All Time Eagles',     'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'RamosLynn',         'team_city': 'St Louis',        'team_name': 'All Time Rams',       'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Showtime718',       'team_city': 'Minnesota',       'team_name': '1998-2000 Vikings',   'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Dazzo0007',         'team_city': 'Green Bay',       'team_name': 'All Time Packers',    'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Drsim80',           'team_city': 'Dallas',          'team_name': 'All Time Cowboys',    'team_wins': '0', 'team_losses': '0'}
]

for team in teams:
    add_team = models.Teams(**team)
    db.session.add(add_team)
    db.session.commit()
    print "%r -- has been added" % (team)
