from app import db, models

games = models.Games.query.all()

for game in games:
    home_stats = models.TeamStats.query.filter_by(team_id=game.home_team).all()
    for hstats in home_stats:
        hstats.games_played = hstats.games_played + 1
        hstats.total_yards = hstats.total_yards + int(game.home_total_yards)
        hstats.passing_yards = hstats.passing_yards + int(game.home_passing_yards)
        hstats.rushing_yards = hstats.rushing_yards + int(game.home_rushing_yards)
        hstats.turnovers = hstats.turnovers + int(game.home_turn_overs)
        hstats.qbr = (hstats.qbr + float(game.home_qbr)) / 2

    away_stats = models.TeamStats.query.filter_by(team_id=game.away_team).all()
    for astats in away_stats:
        astats.games_played = astats.games_played + 1
        astats.total_yards = astats.total_yards + int(game.away_total_yards)
        astats.passing_yards = astats.passing_yards + int(game.away_passing_yards)
        astats.rushing_yards = astats.rushing_yards + int(game.away_rushing_yards)
        astats.turnovers = astats.turnovers + int(game.away_turn_overs)
        astats.qbr = (astats.qbr + float(game.away_qbr)) / 2

    db.session.add(hstats)
    db.session.add(astats)
    db.session.commit()
