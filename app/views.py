from flask import render_template, request, redirect
from app import app, models

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

@app.route('/stats')
def stats():
    return render_template('stats.html',
                            title="Stats")

@app.route('/standings')
def standings():
    teams = models.Teams.query.all()
    return render_template('standings.html',
                            teams=teams,
                            title="Standings")

@app.route('/teams')
def teams():

    return render_template('teams.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=port)
