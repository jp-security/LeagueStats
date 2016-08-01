from flask import render_template, request, redirect
from app import app, models
import json

active_week = "active"

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',
                            title="Home")

@app.route('/games')
def games():
    week = 'All'
    games = models.Games.query.all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week=active_week,
                            games=games)

@app.route('/games/week1')
def week1():
    week = 1
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week1=active_week,
                            games=games)

@app.route('/games/week2')
def week2():
    week = 2
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week2=active_week,
                            games=games)

@app.route('/games/week3')
def week3():
    week = 3
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week3=active_week,
                            games=games)

@app.route('/games/week4')
def week4():
    week = 4
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week4=active_week,
                            games=games)

@app.route('/games/week5')
def week5():
    week = 5
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week5=active_week,
                            games=games)

@app.route('/games/week6')
def week6():
    week = 6
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week6=active_week,
                            games=games)

@app.route('/games/week7')
def week7():
    week = 7
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week7=active_week,
                            games=games)

@app.route('/games/week8')
def week8():
    week = 8
    games = models.Games.query.filter_by(week=week).all()
    return render_template('games.html',
                            title="Games",
                            week=week,
                            active_week8=active_week,
                            games=games)

@app.route('/raw/standings')
def standings_json():
    teams = models.Teams.query.all()

    dataSet = []

    for team in teams:
        team_data = {'owner': team.team_owner, 'team': team.team_name, 'division': team.division, 'wins': team.team_wins, 'losses': team.team_losses}
        dataSet.append(team_data)

    return json.dumps(dataSet)

@app.route('/raw/standings/<division>')
def standings_navy_json(division):
    teams = models.Teams.query.filter_by(division=division).all()

    dataSet = []

    for team in teams:
        team_data = {'owner': team.team_owner, 'team': team.team_name, 'wins': team.team_wins, 'losses': team.team_losses}
        dataSet.append(team_data)

    return json.dumps(dataSet)

@app.route('/raw/stats/offense')
def offense_stats_json():
    offense_stats = models.OffenseTeamStats.query.all()

    offenseDataSet = []

    for team in offense_stats:
        team_stats = {'team': team.team_name, 'games': team.games_played, 'totalyards': team.total_yards,
                    'passingyards': team.passing_yards, 'rushingyards': team.rushing_yards, 'turnovers': team.turnovers,
                    'qbr': team.qbr, 'pointsfor': team.points_scored}
        offenseDataSet.append(team_stats)

    return json.dumps(offenseDataSet)

@app.route('/raw/stats/defense')
def defense_stats_json():
    defense_stats = models.DefenseTeamStats.query.all()

    defenseDataSet = []

    for team in defense_stats:
        team_stats = {'team': team.team_name, 'games': team.games_played, 'totalyards': team.total_yards_against,
                    'passingyards': team.passing_yards_against, 'rushingyards': team.rushing_yards_against, 'turnovers': team.turnovers_forced,
                    'qbr': team.opposing_qbr, 'pointsagaisnt': team.points_allowed}
        defenseDataSet.append(team_stats)

    return json.dumps(defenseDataSet)


@app.route('/stats')
def stats():
    #per_game = (models.OffenseTeamStats.games_played.query.all() - models.OffenseTeamStats.query.

    total_yards = models.OffenseTeamStats.query.with_entities(models.OffenseTeamStats.team_name, models.OffenseTeamStats.total_yards).order_by((models.OffenseTeamStats.total_yards).desc()).limit(3).all()
    passing_yards = models.OffenseTeamStats.query.with_entities(models.OffenseTeamStats.team_name, models.OffenseTeamStats.passing_yards).order_by(models.OffenseTeamStats.passing_yards.desc()).limit(3).all()
    rushing_yards = models.OffenseTeamStats.query.with_entities(models.OffenseTeamStats.team_name, models.OffenseTeamStats.rushing_yards).order_by(models.OffenseTeamStats.rushing_yards.desc()).limit(3).all()
    turnovers = models.OffenseTeamStats.query.with_entities(models.OffenseTeamStats.team_name, models.OffenseTeamStats.turnovers).order_by(models.OffenseTeamStats.turnovers.asc()).limit(3).all()
    qbr = models.OffenseTeamStats.query.with_entities(models.OffenseTeamStats.team_name, models.OffenseTeamStats.qbr).order_by(models.OffenseTeamStats.qbr.desc()).limit(3).all()

    total_yards_allowed = models.OffenseTeamStats.query.with_entities(models.DefenseTeamStats.team_name, models.DefenseTeamStats.total_yards_against).order_by(models.DefenseTeamStats.total_yards_against.asc()).limit(3).all()
    passing_yards_allowed = models.OffenseTeamStats.query.with_entities(models.DefenseTeamStats.team_name, models.DefenseTeamStats.passing_yards_against).order_by(models.DefenseTeamStats.passing_yards_against.asc()).limit(3).all()
    rushing_yards_allowed = models.OffenseTeamStats.query.with_entities(models.DefenseTeamStats.team_name, models.DefenseTeamStats.rushing_yards_against).order_by(models.DefenseTeamStats.rushing_yards_against.asc()).limit(3).all()
    turnovers_forced = models.OffenseTeamStats.query.with_entities(models.DefenseTeamStats.team_name, models.DefenseTeamStats.turnovers_forced).order_by(models.DefenseTeamStats.turnovers_forced.desc()).limit(3).all()
    opposing_qbr = models.OffenseTeamStats.query.with_entities(models.DefenseTeamStats.team_name, models.DefenseTeamStats.opposing_qbr).order_by(models.DefenseTeamStats.opposing_qbr.asc()).limit(3).all()

    return render_template('stats.html',
                            title='Stats',
                            total_yards=total_yards,
                            passing_yards=passing_yards,
                            rushing_yards=rushing_yards,
                            turnovers=turnovers,
                            qbr=qbr,
                            total_yards_allowed=total_yards_allowed,
                            passing_yards_allowed=passing_yards_allowed,
                            rushing_yards_allowed=rushing_yards_allowed,
                            turnovers_forced=turnovers_forced,
                            opposing_qbr=opposing_qbr)


@app.route('/stats/offense')
def offense_stats():
    return render_template('offensestats.html',
                            title="Stats")

@app.route('/stats/defense')
def defense_stats():
    return render_template('defensestats.html',
                            title="Stats")

@app.route('/standings')
def standings():
    return render_template('standings.html',
                            title="Standings")

@app.route('/standings/navy')
def navy_standings():
    return render_template('navystandings.html',
                            title="Navy Standings")

@app.route('/standings/gold')
def gold_standings():
    return render_template('goldstandings.html',
                            title="Gold Standings")


@app.route('/team/<teamname>')
def team(teamname):
    team = models.Teams.query.filter_by(team_name=teamname).all()

    for t in team:
        offense = models.OffenseTeamStats.query.filter_by(team_id=t.id).first()
        defense = models.DefenseTeamStats.query.filter_by(team_id=t.id).first()

    return render_template('teams.html',
                            team=team,
                            active=teamname,
                            offense=offense,
                            defense=defense)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(port=port)
