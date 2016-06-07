from app import models, db

teams = models.Teams.query.all()

for team in teams:
    stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'total_yards': 0, 'passing_yards': 0, 'rushing_yards': 0, 'turnovers': 0, 'qbr': 0}
    add_team = models.TeamStats(**stats_create)
    db.session.add(add_team)
    db.session.commit()
    print "%r -- stats entry created" % (team)
