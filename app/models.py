from datetime import datetime
import hashlib
from . import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission:
    LOGIN = 0x01
    ADDGAMES = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.LOGIN, True),
            'Moderator': (Permission.LOGIN |
                          Permission.ADDGAMES, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    game_entry = db.relationship('Games', back_populates='author')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['CAG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Teams(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_owner = db.Column(db.String(256), unique=True)
    team_city = db.Column(db.String(256))
    team_name = db.Column(db.String(256), unique=True)
    division = db.Column(db.String(256))
    team_wins = db.Column(db.Integer)
    team_losses = db.Column(db.Integer)

    home = db.relationship('Games', lazy='joined', foreign_keys='Games.home_team', backref='home_game')
    away = db.relationship('Games', lazy='joined', foreign_keys='Games.away_team', backref='away_game')

    def __repr__(self):
        return '<%r %r %r %r %r %r %r>' % (self.id, self.team_owner, self.team_city, self.team_name, self.division, self.team_wins, self.team_losses)
        #return '<%r %r>' % (self.home, self.away)

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='game_entry')

    home_team = db.Column(db.Integer, db.ForeignKey('teams.id'))
    home_score = db.Column(db.Integer)
    home_total_yards = db.Column(db.Integer)
    home_passing_yards = db.Column(db.Integer)
    home_rushing_yards = db.Column(db.Integer)
    home_turn_overs = db.Column(db.Integer)
    home_qbr = db.Column(db.Float)

    away_team = db.Column(db.Integer, db.ForeignKey('teams.id'))
    away_score = db.Column(db.Integer)
    away_total_yards = db.Column(db.Integer)
    away_passing_yards = db.Column(db.Integer)
    away_rushing_yards = db.Column(db.Integer)
    away_turn_overs = db.Column(db.Integer)
    away_qbr = db.Column(db.Float)

    home = db.relationship('Teams', lazy='joined', foreign_keys='Games.home_team', backref='game_ashome')
    away = db.relationship('Teams', lazy='joined', foreign_keys='Games.away_team', backref='game_asaway')

    def __repr__(self):
        if self.home_score > self.away_score:
            final = str(self.home.team_name) + ' defeats ' + str(self.away.team_name) + ' ' + str(self.home_score) + ' to ' + str(self.away_score)
        else:
            final = str(self.away.team_name) + ' defeats ' + str(self.home.team_name) + ' ' + str(self.away_score) + ' to ' + str(self.home_score)

        return ('%r \n'
                '<Home Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r>\n'
                '<Away Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r>'
                % (final
                , self.home, self.home_total_yards, self.home_passing_yards, self.home_rushing_yards, self.home_turn_overs, self.home_qbr
                , self.away, self.away_total_yards, self.away_passing_yards, self.away_rushing_yards, self.away_turn_overs, self.away_qbr))

class OffenseTeamStats(db.Model):
    __tablename__ = 'offenseteamstats'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_name = db.Column(db.String(256))
    games_played = db.Column(db.Integer)
    no_stats_game = db.Column(db.Integer)
    points_scored = db.Column(db.Integer)

    total_yards = db.Column(db.Integer)
    passing_yards = db.Column(db.Integer)
    rushing_yards = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    qbr = db.Column(db.Float)

    def __repr__(self):
        return ('Team: %r - Games Played: %r - Total Yards: %r - Passing Yards: %r - Rushing Yards: %r - Turnovers: %r - QBR: %r'
                % (self.team, self.games_played, self.total_yards, self.passing_yards, self.rushing_yards, self.turnovers, self.qbr))

class DefenseTeamStats(db.Model):
    __tablename__ = 'defenseteamstats'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_name = db.Column(db.String(256))
    games_played = db.Column(db.Integer)
    no_stats_game = db.Column(db.Integer)
    points_allowed = db.Column(db.Integer)

    total_yards_against = db.Column(db.Integer)
    passing_yards_against = db.Column(db.Integer)
    rushing_yards_against = db.Column(db.Integer)
    turnovers_forced = db.Column(db.Integer)
    opposing_qbr = db.Column(db.Float)

    def __repr__(self):
        return ('Team: %r - Games Played: %r - Total Yards: %r - Passing Yards: %r - Rushing Yards: %r - Turnovers: %r - QBR: %r'
                % (self.team, self.games_played, self.total_yards, self.passing_yards, self.rushing_yards, self.turnovers, self.qbr))
