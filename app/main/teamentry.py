from . import main
from .. import db
import app.models as models

def teamAdd():
    teams = [
    {'team_owner': 'OWNER NAME HERE',   'team_city': 'TEAM CITY HERE',      'team_name': 'TEAM NAME HERE',        'division': 'DIVISION HERE',      'team_wins': '0', 'team_losses': '0'},
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
