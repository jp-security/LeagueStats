from app import models, db

week = raw_input('Enter the week of the game: ')
home_team = raw_input('Enter the Home Team: ')
home_score = raw_input('Enter the Home Team Score: ')
home_total_yards = raw_input('Enter the Home Team Total Yards: ')
home_passing_yards = raw_input('Enter the Home Team Passing Yards: ')
home_rushing_yards = raw_input('Enter the Home Team Rushing Yards: ')
home_turn_overs = raw_input('Enter the Home Team Turnovers: ')
home_qbr = raw_input('Enter the Home Team QBR: ')
away_team = raw_input('Enter the Away Team: ')
away_score = raw_input('Enter the Away Team Score: ')
away_total_yards = raw_input('Enter the Away Team Total Yards: ')
away_passing_yards = raw_input('Enter the Away Team Passing Yards: ')
away_rushing_yards = raw_input('Enter the Away Team Rushing Yards: ')
away_turn_overs = raw_input('Enter the Away Team Turnovers: ')
away_qbr = raw_input('Enter the Away Team QBR: ')

home_team
home_team = models.Teams.query.filter_by(team_name=home_team).all()
for h in home_team:
    home_team_id = int(h.id)

away_team = models.Teams.query.filter_by(team_name=away_team).all()
for a in away_team:
    away_team_id = int(a.id)

game_stats = {
'week': week,
'home_team': home_team_id,
'away_team': away_team_id,
'home_score': home_score,
'away_score': away_score,
'home_total_yards': home_total_yards,
'home_passing_yards': home_passing_yards,
'home_rushing_yards': home_rushing_yards,
'home_turn_overs': home_turn_overs,
'home_qbr': home_qbr,
'away_total_yards': away_total_yards,
'away_passing_yards': away_passing_yards,
'away_rushing_yards': away_rushing_yards,
'away_turn_overs': away_turn_overs,
'away_qbr': away_qbr
}

if home_score > away_score:
    for h in home_team:
        h.team_wins = h.team_wins + 1

    for a in away_team:
        a.team_losses = a.team_losses + 1

else:
    for h in home_team:
        h.team_losses = h.team_losses + 1

    for a in away_team:
        a.team_wins = a.team_wins + 1

game = models.Games(**game_stats)
db.session.add(game)
db.session.add(h)
db.session.add(a)
db.session.commit()
