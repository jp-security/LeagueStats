from . import main
from .. import db
import app.models as models

def teamAdd(owner, city, name, division, wins, losses):
    teams = [
    {'team_owner': 'Darklord Destro',   'team_city': 'Washington',      'team_name': "91 Redskins",        'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'tjspeaks',          'team_city': 'Baltimore',       'team_name': "67 Colts",          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'Aquick Assasin',    'team_city': 'Cleveland',       'team_name': "64 Browns",          'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'MightyRx',          'team_city': 'New Orleans',     'team_name': "67 Saints",          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'Dazzo47',           'team_city': 'Chicago',         'team_name': "66 Bears",           'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'SitnHereFlossin',   'team_city': 'Tampa Bay',       'team_name': "99 Bucs",            'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'Pcat Magoo',        'team_city': 'Kansas City',     'team_name': "90 Chiefs",          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'xRun and Sh00tx',   'team_city': 'Houston',         'team_name': "93 Oilers",          'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'HeavyHitter55',     'team_city': 'Philadelphia',    'team_name': "50 Eagles",          'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'RamosLynn',         'team_city': 'Denver',          'team_name': "98 Broncos",         'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'Dazzo0007',         'team_city': 'Chicago',         'team_name': "85 Bears",           'division': 'Gold',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'Bengal1fan2',       'team_city': 'St. Louis',       'team_name': "00 Rams",            'division': 'Navy',      'team_wins': '0', 'team_losses': '0'},
    {'team_owner': 'ElectricAggie',     'team_city': 'Dallas',          'team_name': "93 Cowboys",         'division': 'Navy',      'team_wins': '0', 'team_losses': '0'}
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

if __name__ == "__main__":
    teamAdd()
