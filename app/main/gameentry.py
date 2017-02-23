from . import main
from .. import db
import app.models as models

def NoStats(week, added_by, winning_team, home_team, home_score, away_team, away_score):
    home_team = models.Teams.query.filter_by(team_name=home_team).all()
    for h in home_team:
        home_team_id = int(h.id)

    away_team = models.Teams.query.filter_by(team_name=away_team).all()
    for a in away_team:
        away_team_id = int(a.id)

    home_total_yards = 0
    home_passing_yards = 0
    home_rushing_yards = 0
    home_turn_overs = 0
    home_qbr = 0

    away_total_yards = 0
    away_passing_yards = 0
    away_rushing_yards = 0
    away_turn_overs = 0
    away_qbr = 0

    game_stats = {
    'week': week,
    'added_by': added_by,
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

    offense_home_stats = models.OffenseTeamStats.query.filter_by(team_id=home_team_id).all()
    for ohstats in offense_home_stats:
        ohstats.games_played = ohstats.games_played + 1
        ohstats.no_stats_game = ohstats.no_stats_game + 1
        ohstats.points_scored = ohstats.points_scored + int(home_score)

    defense_home_stats = models.DefenseTeamStats.query.filter_by(team_id=home_team_id).all()
    for dhstats in defense_home_stats:
        dhstats.games_played = dhstats.games_played + 1
        dhstats.no_stats_game = dhstats.no_stats_game + 1
        dhstats.points_allowed = dhstats.points_allowed + int(away_score)

    offense_away_stats = models.OffenseTeamStats.query.filter_by(team_id=away_team_id).all()
    for oastats in offense_away_stats:
        oastats.games_played = oastats.games_played + 1
        oastats.no_stats_game = oastats.no_stats_game + 1
        oastats.points_scored = oastats.points_scored + int(away_score)

    defense_away_stats = models.DefenseTeamStats.query.filter_by(team_id=away_team_id).all()
    for dastats in defense_away_stats:
        dastats.games_played = dastats.games_played + 1
        dastats.no_stats_game = dastats.no_stats_game + 1
        dastats.points_allowed = dastats.points_allowed + int(home_score)

    if winning_team == 'Home':
        for h in home_team:
            h.team_wins = h.team_wins + 1

        for a in away_team:
            a.team_losses = a.team_losses + 1

    elif winning_team == 'Away':
        for h in home_team:
            h.team_losses = h.team_losses + 1

        for a in away_team:
            a.team_wins = a.team_wins + 1

    game = models.Games(**game_stats)
    db.session.add(game)
    db.session.add(h)
    db.session.add(ohstats)
    db.session.add(dhstats)
    db.session.add(a)
    db.session.add(oastats)
    db.session.add(dastats)

def Stats(week, added_by, winning_team, home_team, home_score, home_passing_yards, home_rushing_yards, home_turn_overs, home_qbr,
            away_team, away_score, away_passing_yards, away_rushing_yards, away_turn_overs, away_qbr):
    home_team = models.Teams.query.filter_by(team_name=home_team).all()
    for h in home_team:
        home_team_id = int(h.id)

    away_team = models.Teams.query.filter_by(team_name=away_team).all()
    for a in away_team:
        away_team_id = int(a.id)

    home_total_yards = home_passing_yards + home_rushing_yards
    home_passing_yards = home_passing_yards
    home_rushing_yards = home_rushing_yards
    home_turn_overs = home_turn_overs
    home_qbr = home_qbr

    away_total_yards = away_passing_yards + away_rushing_yards
    away_passing_yards = away_passing_yards
    away_rushing_yards = away_rushing_yards
    away_turn_overs = away_turn_overs
    away_qbr = away_qbr

    game_stats = {
    'week': week,
    'added_by': added_by,
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

    offense_home_stats = models.OffenseTeamStats.query.filter_by(team_id=home_team_id).all()
    for ohstats in offense_home_stats:
        ohstats.games_played = ohstats.games_played + 1
        ohstats.points_scored = ohstats.points_scored + int(home_score)
        ohstats.total_yards = ohstats.total_yards + int(home_total_yards)
        ohstats.passing_yards = ohstats.passing_yards + int(home_passing_yards)
        ohstats.rushing_yards = ohstats.rushing_yards + int(home_rushing_yards)
        ohstats.turnovers = ohstats.turnovers + int(home_turn_overs)
        if ohstats.qbr == 0:
            ohstats.qbr = home_qbr
        else:
            ohstats.qbr = round((ohstats.qbr + float(home_qbr)) / 2, 1)

    defense_home_stats = models.DefenseTeamStats.query.filter_by(team_id=home_team_id).all()
    for dhstats in defense_home_stats:
        dhstats.games_played = dhstats.games_played + 1
        dhstats.points_allowed = dhstats.points_allowed + int(away_score)
        dhstats.total_yards_against = dhstats.total_yards_against + int(away_total_yards)
        dhstats.passing_yards_against = dhstats.passing_yards_against + int(away_passing_yards)
        dhstats.rushing_yards_against = dhstats.rushing_yards_against + int(away_rushing_yards)
        dhstats.turnovers_forced = dhstats.turnovers_forced + int(away_turn_overs)
        if dhstats.opposing_qbr == 0:
            dhstats.opposing_qbr = away_qbr
        else:
            dhstats.opposing_qbr = round((dhstats.opposing_qbr + float(away_qbr)) / 2, 1)

    offense_away_stats = models.OffenseTeamStats.query.filter_by(team_id=away_team_id).all()
    for oastats in offense_away_stats:
        oastats.games_played = oastats.games_played + 1
        oastats.points_scored = oastats.points_scored + int(away_score)
        oastats.total_yards = oastats.total_yards + int(away_total_yards)
        oastats.passing_yards = oastats.passing_yards + int(away_passing_yards)
        oastats.rushing_yards = oastats.rushing_yards + int(away_rushing_yards)
        oastats.turnovers = oastats.turnovers + int(away_turn_overs)
        if oastats.qbr == 0:
            oastats.qbr = away_qbr
        else:
            oastats.qbr = round((oastats.qbr + float(away_qbr)) / 2, 1)

    defense_away_stats = models.DefenseTeamStats.query.filter_by(team_id=away_team_id).all()
    for dastats in defense_away_stats:
        dastats.games_played = dastats.games_played + 1
        dastats.points_allowed = dastats.points_allowed + int(home_score)
        dastats.total_yards_against = dastats.total_yards_against + int(home_total_yards)
        dastats.passing_yards_against = dastats.passing_yards_against + int(home_passing_yards)
        dastats.rushing_yards_against = dastats.rushing_yards_against + int(home_rushing_yards)
        dastats.turnovers_forced = dastats.turnovers_forced + int(home_turn_overs)
        if dastats.opposing_qbr == 0:
            dastats.opposing_qbr = home_qbr
        else:
            dastats.opposing_qbr = round((dastats.opposing_qbr + float(home_qbr)) / 2, 1)

    if winning_team == 'Home':
        for h in home_team:
            h.team_wins = h.team_wins + 1

        for a in away_team:
            a.team_losses = a.team_losses + 1

    elif winning_team == 'Away':
        for h in home_team:
            h.team_losses = h.team_losses + 1

        for a in away_team:
            a.team_wins = a.team_wins + 1

    game = models.Games(**game_stats)
    db.session.add(game)
    db.session.add(h)
    db.session.add(ohstats)
    db.session.add(dhstats)
    db.session.add(a)
    db.session.add(oastats)
    db.session.add(dastats)
