from app import db

class Teams(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_owner = db.Column(db.String(256))
    team_city = db.Column(db.String(256))
    team_name = db.Column(db.String(256))
    team_wins = db.Column(db.Integer)
    team_losses = db.Column(db.Integer)

    home = db.relationship('Games', lazy='joined', foreign_keys='Games.home_team', backref='home_game')
    away = db.relationship('Games', lazy='joined', foreign_keys='Games.away_team', backref='away_game')

    def __repr__(self):
        return '<%r %r %r %r %r %r>' % (self.id, self.team_owner, self.team_city, self.team_name, self.team_wins, self.team_losses)
        #return '<%r %r>' % (self.home, self.away)

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)

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
            final = str(self.home) + ' defeats ' + str(self.away) + ' ' + str(self.home_score) + ' to ' + str(self.away_score)
        else:
            final = str(self.away) + ' defeats ' + str(self.home) + ' ' + str(self.away_score) + ' to ' + str(self.home_score)

        return ('%r \n'
                '<Home Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r>\n'
                '<Away Team - %r: Total Yards - %r Passing Yards - %r Rushing Yards - %r Tunrovers - %r QBR - %r>'
                % (final
                , self.home, self.home_total_yards, self.home_passing_yards, self.home_rushing_yards, self.home_turn_overs, self.home_qbr
                , self.away, self.away_total_yards, self.away_passing_yards, self.away_rushing_yards, self.away_turn_overs, self.away_qbr))
