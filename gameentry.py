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

home_stats = models.TeamStats.query.filter_by(team=home_team_id).all()
for hstats in home_stats:
    hstats.games_played = hstats.games_played + 1
    hstats.total_yards = hstats.total_yards + int(home_total_yards)
    hstats.passing_yards = hstats.passing_yards + int(home_passing_yards)
    hstats.rushing_yards = hstats.rushing_yards + int(home_rushing_yards)
    hstats.turnovers = hstats.turnovers + int(home_turn_overs)
    hstats.qbr = (hstats.qbr + float(home_qbr)) / 2

away_stats = models.TeamStats.query.filter_by(team=away_team_id).all()
for astats in away_stats:
    astats.games_played = astats.games_played + 1
    astats.total_yards = astats.total_yards + int(away_total_yards)
    astats.passing_yards = astats.passing_yards + int(away_passing_yards)
    astats.rushing_yards = astats.rushing_yards + int(away_rushing_yards)
    astats.turnovers = astats.turnovers + int(away_turn_overs)
    astats.qbr = (astats.qbr + float(away_qbr)) / 2

game = models.Games(**game_stats)
db.session.add(game)
db.session.add(h)
db.session.add(hstats)
db.session.add(a)
db.session.add(astats)
db.session.commit()
