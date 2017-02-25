from datetime import datetime
import json
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from .gameentry import NoStats, Stats
from .database import LastFive
from .forms import GameInformation, TeamEntry, EditProfileAdminForm, EditProfileForm
from .teamentry import teamAdd
from . import main
from .. import db
import app.models as models
from app.models import User, Role, Permission
from ..decorators import admin_required, permission_required

active_week = "active"

@main.route('/team-entry', methods=['GET', 'POST'])
@login_required
@admin_required
def team_entry():
    form = TeamEntry()
    if form.validate_on_submit():
        teamAdd()
        return redirect(url_for('main.home'))
    return render_template('main/teamentry.html', form=form)

@main.route('/game-entry', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADDGAMES)
def game_entry():
    form = GameInformation()
    form.added_by = current_user.id
    last_five = LastFive()

    if form.validate_on_submit():
        if form.no_stats.data == 'Yes':
            NoStats(form.week.data, form.added_by, form.winning_team.data, form.home_team.data, form.home_score.data, form.away_team.data, form.away_score.data)
        elif form.no_stats.data == 'No':
            Stats(form.week.data, form.added_by, form.winning_team.data, form.home_team.data, form.home_score.data, form.home_passing_yards.data, form.home_rushing_yards.data,
                    form.home_turn_overs.data, form.home_qbr.data, form.away_team.data, form.away_score.data, form.away_passing_yards.data,
                    form.away_rushing_yards.data, form.away_turn_overs.data, form.away_qbr.data)
        else:
            flash('There were errors submitting the game results')
        return redirect(url_for('main.game_entry'))
    return render_template('main/gameentry.html', form=form, last_five=last_five)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    return render_template('main/edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    return render_template('main/edit_profile.html', form=form, user=user)

@main.route('/')
@main.route('/home')
def home():
    last_five = LastFive()
    return render_template('main/index.html',
                            title="Home", last_five=last_five)

@main.route('/games')
def games():
    week = 'All'
    games = models.Games.query.all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week=active_week,
                            games=games)

@main.route('/games/week1')
def week1():
    week = 1
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week1=active_week,
                            games=games)

@main.route('/games/week2')
def week2():
    week = 2
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week2=active_week,
                            games=games)

@main.route('/games/week3')
def week3():
    week = 3
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week3=active_week,
                            games=games)

@main.route('/games/week4')
def week4():
    week = 4
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week4=active_week,
                            games=games)

@main.route('/games/week5')
def week5():
    week = 5
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week5=active_week,
                            games=games)

@main.route('/games/week6')
def week6():
    week = 6
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week6=active_week,
                            games=games)

@main.route('/games/week7')
def week7():
    week = 7
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week7=active_week,
                            games=games)

@main.route('/games/week8')
def week8():
    week = 8
    games = models.Games.query.filter_by(week=week).all()
    return render_template('main/games.html',
                            title="Games",
                            week=week,
                            active_week8=active_week,
                            games=games)

@main.route('/raw/standings')
def standings_json():
    teams = models.Teams.query.all()

    dataSet = []

    for team in teams:
        team_data = {'owner': team.team_owner, 'team': team.team_name, 'division': team.division, 'wins': team.team_wins, 'losses': team.team_losses}
        dataSet.append(team_data)

    return json.dumps(dataSet)

@main.route('/raw/standings/<division>')
def standings_navy_json(division):
    teams = models.Teams.query.filter_by(division=division).all()

    dataSet = []

    for team in teams:
        team_data = {'owner': team.team_owner, 'team': team.team_name, 'wins': team.team_wins, 'losses': team.team_losses}
        dataSet.append(team_data)

    return json.dumps(dataSet)

@main.route('/raw/stats/offense')
def offense_stats_json():
    offense_stats = models.OffenseTeamStats.query.all()

    offenseDataSet = []

    for team in offense_stats:
        team_stats = {'team': team.team_name, 'games': team.games_played, 'totalyards': team.total_yards,
                    'passingyards': team.passing_yards, 'rushingyards': team.rushing_yards, 'turnovers': team.turnovers,
                    'qbr': team.qbr, 'pointsfor': team.points_scored}
        offenseDataSet.append(team_stats)

    return json.dumps(offenseDataSet)

@main.route('/raw/stats/defense')
def defense_stats_json():
    defense_stats = models.DefenseTeamStats.query.all()

    defenseDataSet = []

    for team in defense_stats:
        team_stats = {'team': team.team_name, 'games': team.games_played, 'totalyards': team.total_yards_against,
                    'passingyards': team.passing_yards_against, 'rushingyards': team.rushing_yards_against, 'turnovers': team.turnovers_forced,
                    'qbr': team.opposing_qbr, 'pointsagaisnt': team.points_allowed}
        defenseDataSet.append(team_stats)

    return json.dumps(defenseDataSet)


@main.route('/stats')
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

    return render_template('main/stats.html',
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


@main.route('/stats/offense')
def offense_stats():
    return render_template('main/offensestats.html',
                            title="Stats")

@main.route('/stats/defense')
def defense_stats():
    return render_template('main/defensestats.html',
                            title="Stats")

@main.route('/standings')
def standings():
    return render_template('main/standings.html',
                            title="Standings")

@main.route('/standings/navy')
def navy_standings():
    return render_template('main/navystandings.html',
                            title="Navy Standings")

@main.route('/standings/gold')
def gold_standings():
    return render_template('main/goldstandings.html',
                            title="Gold Standings")


@main.route('/team/<teamname>')
def team(teamname):
    team = models.Teams.query.filter_by(team_name=teamname).all()

    for t in team:
        offense = models.OffenseTeamStats.query.filter_by(team_id=t.id).first()
        defense = models.DefenseTeamStats.query.filter_by(team_id=t.id).first()

    return render_template('main/teams.html',
                            team=team,
                            active=teamname,
                            offense=offense,
                            defense=defense)
