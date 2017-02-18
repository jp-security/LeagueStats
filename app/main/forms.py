from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange

class TeamEntry(FlaskForm):
    submit = SubmitField('Add Teams ')

class GameInformation(FlaskForm):
    teams = [('Browns', 'Browns'),
            ('Ravens', 'Ravens'),
            ('Redskins', 'Redskins'),
            ('Chargers', 'Chargers'),
            ('Buccaneers', 'Buccaneers'),
            ('Bears', 'Bears'),
            ('Bengals', 'Bengals'),
            ('Chiefs', 'Chiefs'),
            ('Oilers', 'Oilers')]

    no_stats = SelectField('No Stats', choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    week = IntegerField('Week', validators=[Required(), NumberRange(0, 16)])

    home_team = SelectField('Home Team', choices=teams)
    home_score = IntegerField('Home Score', validators=[Required(), NumberRange(0,100)])

    away_team = SelectField('Away Team', choices=teams)
    away_score = IntegerField('Away Score', validators=[Required(), NumberRange(0,100)])

    winning_team = SelectField('Winning Team', choices=[('Home', 'Home'), ('Away', 'Away')])

    home_passing_yards = IntegerField('Home Passing Yards', validators=[Required(), NumberRange(0,1000)], default=0)
    home_rushing_yards = IntegerField('Home Rushing Yards', validators=[Required(), NumberRange(0,1000)], default=0)
    home_turn_overs = IntegerField('Home Turnovers', validators=[NumberRange(0,10)], default=0)
    home_qbr = DecimalField('Home QBR', validators=[Required()], default=0)

    away_passing_yards = IntegerField('Away Passing Yards', validators=[Required(), NumberRange(0,1000)], default=0)
    away_rushing_yards = IntegerField('Away Rushing Yards', validators=[Required(), NumberRange(0,1000)], default=0)
    away_turn_overs = IntegerField('Away Turnovers', validators=[NumberRange(0,10)], default=0)
    away_qbr = DecimalField('Away QBR', validators=[Required()], default=0)

    submit = SubmitField('Add Game')

class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                'Usernames must have only letters, '
                                                                                'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Submit')

    def __int__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        print self.role.choices
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
