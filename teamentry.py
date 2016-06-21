from app import models, db

teams = [
{'team_owner': 'Darklord Destro',   'team_city': 'Washington',      'team_name': 'Redskins',        'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'tjspeaks',          'team_city': 'Baltimore',       'team_name': 'Ravens',          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Aquick Assasin',    'team_city': 'Cleveland',       'team_name': 'Browns',          'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'MightyRx',          'team_city': 'San Diego',       'team_name': 'Chargers',        'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'RebelRouser1988',   'team_city': 'Tampa Bay',       'team_name': 'Buccanneers',     'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Dazzo47',           'team_city': 'Chicago',         'team_name': 'Bears',           'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'SitnHereFlossin',   'team_city': 'Cincinnati',      'team_name': 'Bengals',         'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Pcat Magoo',        'team_city': 'Kansas City',     'team_name': 'Chiefs',          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'xRun and Sh00tx',   'team_city': 'Houston',         'team_name': 'Oilers',          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'HeavyHitter55',     'team_city': 'Philadelphia',    'team_name': 'Eagles',          'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'RamosLynn',         'team_city': 'Seattle',         'team_name': 'Seahawks',        'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Showtime718',       'team_city': 'Minnesota',       'team_name': 'Vikings',         'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Dazzo0007',         'team_city': 'Green Bay',       'team_name': 'Packers',         'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Saltyseadog93',     'team_city': 'Detriot',         'team_name': 'Lions',           'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Jokerpac32',        'team_city': 'Oakland',         'team_name': 'Raiders',         'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'fifty six',         'team_city': 'Miami',           'team_name': 'Dolphins',        'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'Touchdown56',       'team_city': 'Pittsburgh',      'team_name': 'Steelers',        'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
{'team_owner': 'GeDDeN',            'team_city': 'New York',        'team_name': 'Giants',          'division': 'Navy',      'team_wins': '0', 'team_losses': '0'}
]

for team in teams:
    add_team = models.Teams(**team)
    db.session.add(add_team)
    db.session.commit()
    print "%r -- has been added" % (team)

teams = models.Teams.query.all()

for team in teams:
    offense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_scored': 0, 'total_yards': 0, 'passing_yards': 0, 'rushing_yards': 0, 'turnovers': 0, 'qbr': 0}
    defense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_allowed': 0, 'total_yards_against': 0, 'passing_yards_against': 0, 'rushing_yards_against': 0, 'turnovers_forced': 0, 'opposing_qbr': 0}

    offense_add_team = models.OffenseTeamStats(**offense_stats_create)
    defense_add_team = models.DefenseTeamStats(**defense_stats_create)
    db.session.add(offense_add_team)
    db.session.add(defense_add_team)
    db.session.commit()
    print "%r -- stats entry created" % (team)
