from . import main
from .. import db
import app.models as models

def LastFive():
    query = models.Games.query.order_by(models.Games.id.desc()).limit(5).all()
    return query

def addTeam(owner, city, name, division):
    team = {'team_owner': owner, 'team_city': city, 'team_name': name, 'division': division, 'team_wins': '0', 'team_losses': '0'}
    add_team = models.Teams(**team)
    db.session.add(add_team)
    db.session.commit()

    for team in models.Teams.query.filter_by(team_name=name):
        try:
            team_history = {
            'team_owner': team.team_owner,
            'seasons_played': 0,
            'games_played': 0,
            'owner_wins': 0,
            'owner_losses': 0,
            'points_scored': 0,
            'total_yards': 0,
            'passing_yards': 0,
            'rushing_yards': 0,
            'turnovers': 0,
            'qbr': 0,
            'points_allowed': 0,
            'total_yards_against': 0,
            'passing_yards_against': 0,
            'rushing_yards_against': 0,
            'turnovers_forced': 0,
            'opposing_qbr': 0
            }

            history = models.HistoricalStats(**team_history)
            db.session.add(history)
            db.session.commit()

            offense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_scored': 0, 'total_yards': 0, 'passing_yards': 0, 'rushing_yards': 0, 'turnovers': 0, 'qbr': 0}
            defense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_allowed': 0, 'total_yards_against': 0, 'passing_yards_against': 0, 'rushing_yards_against': 0, 'turnovers_forced': 0, 'opposing_qbr': 0}

            offense_add_team = models.OffenseTeamStats(**offense_stats_create)
            defense_add_team = models.DefenseTeamStats(**defense_stats_create)
            db.session.add(offense_add_team)
            db.session.add(defense_add_team)
            db.session.commit()

            return
        except:
            db.session.rollback()
            pass

        offense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_scored': 0, 'total_yards': 0, 'passing_yards': 0, 'rushing_yards': 0, 'turnovers': 0, 'qbr': 0}
        defense_stats_create = {'team_id': team.id, 'team_name': team.team_name, 'games_played': 0, 'no_stats_game': 0, 'points_allowed': 0, 'total_yards_against': 0, 'passing_yards_against': 0, 'rushing_yards_against': 0, 'turnovers_forced': 0, 'opposing_qbr': 0}

        offense_add_team = models.OffenseTeamStats(**offense_stats_create)
        defense_add_team = models.DefenseTeamStats(**defense_stats_create)
        db.session.add(offense_add_team)
        db.session.add(defense_add_team)
        db.session.commit()

        return

def newSeason():
    models.OffenseTeamStats.query.delete()
    models.DefenseTeamStats.query.delete()
    models.Games.query.delete()
    models.Teams.query.delete()
    db.session.commit()

def historicalStats():
    #This section will move all the stats from the current season to a historical category

    #Pull Offensive and Defensive Stats, along with Wins/Losses
    #Have a Per Season Category

    for team in models.Teams.query.all():
        for offense in models.OffenseTeamStats.query.filter_by(team_id=team.id):
            for defense in models.DefenseTeamStats.query.filter_by(team_id=team.id):
                for history in models.HistoricalStats.query.filter_by(team_owner=team.team_owner):
                    try:
                        history.seasons_played = history.seasons_played + 1
                        history.games_played = history.games_played + offense.games_played
                        history.owner_wins = history.owner_wins + team.team_wins
                        history.owner_losses = history.owner_losses + team.team_losses

                        history.points_scored = history.points_scored + offense.points_scored
                        history.total_yards = history.total_yards + offense.total_yards
                        history.passing_yards = history.passing_yards + offense.passing_yards
                        history.rushing_yards = history.rushing_yards + offense.rushing_yards
                        history.turnovers = history.turnovers + offense.turnovers
                        history.qbr = history.qbr + offense.qbr

                        history.points_allowed = history.points_allowed + defense.points_allowed
                        history.total_yards_against = history.total_yards_against + defense.total_yards_against
                        history.passing_yards_against = history.passing_yards_against + defense.passing_yards_against
                        history.rushing_yards_against = history.rushing_yards_against + defense.rushing_yards_against
                        history.turnovers_forced = history.turnovers_forced + defense.turnovers_forced
                        history.opposing_qbr = history.opposing_qbr + defense.opposing_qbr

                        newSeason()
                    except Exception as e:
                        print e
