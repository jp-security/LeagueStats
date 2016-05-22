from app import db

class Teams(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    team_city = db.Column(db.String(256))
    team_name = db.Column(db.String(256))

    def __repr__(self):
        return '<%r %r %r>' % (self.id, self.team_city, self.team_name)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)

    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_total_yards = db.Column(db.Integer)
    home_passing_yards = db.Column(db.Integer)
    home_rushing_yards = db.Column(db.Integer)
    home_turn_overs = db.Column(db.Integer)
    home_qbr = db.Column(db.Float)

    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_total_yards = db.Column(db.Integer)
    away_passing_yards = db.Column(db.Integer)
    away_rushing_yards = db.Column(db.Integer)
    away_turn_overs = db.Column(db.Integer)
    away_qbr = db.Column(db.Float)

    home = db.relationship('Teams', lazy='joined', foreign_keys='Game.home_team', backref='game_ashome')
    away = db.relationship('Teams', lazy='joined', foreign_keys='Game.away_team', backref='game_asaway')

    def __repr__(self):
        return ('<Home Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r'
                'Away Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r'
                % (self.home, self.home_total_yards, self.home_passing_yards, self.home_rushing_yards, self.home_turn_overs, self.home_qbr
                , self.away, self.away_total_yards, self.away_passing_yards, self.away_rushing_yards, self.away_turn_overs, self.away_qbr))
