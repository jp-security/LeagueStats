from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, IntegerField, DecimalField, HiddenField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from ..models import Role, User

class TeamEntry(FlaskForm):
    submit = SubmitField('Add Teams ')

class GameInformation(FlaskForm):
    teams = [("'91 Redskins", "'91 Redskins"),
            ("'67 Colts'", "'67 Colts'"),
            ("'64 Browns", "'64 Browns"),
            ("'67 Saints", "'67 Saints"),
            ("'67 Bears", "'67 Bears"),
            ("'99 Bucs", "'99 Bucs"),
            ("'90 Chiefs", "'90 Chiefs"),
            ("'93 Oilers", "'93 Oilers"),
            ("'98 Broncos", "'98 Broncos"),
            ("'85 Bears", "'85 Bears"),
            ("'00 Rams", "'00 Rams"),
            ("'93 Cowboys", "'93 Cowboys"),
            ("'50 Eagles", "'50 Eagles")]

    no_stats = SelectField('No Stats', choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    week = IntegerField('Week', validators=[Required(), NumberRange(0, 16)])
    added_by = HiddenField('Added By')

    home_team = SelectField('Home Team', choices=teams)
    home_score = IntegerField('Home Score', validators=[Required(), NumberRange(0,100)])

    away_team = SelectField('Away Team', choices=teams)
    away_score = IntegerField('Away Score', validators=[Required(), NumberRange(0,100)])

    winning_team = SelectField('Winning Team', choices=[('Home', 'Home'), ('Away', 'Away')])

    home_passing_yards = IntegerField('Home Passing Yards', validators=[NumberRange(0,1000)], default=0)
    home_rushing_yards = IntegerField('Home Rushing Yards', validators=[NumberRange(0,1000)], default=0)
    home_turn_overs = IntegerField('Home Turnovers', validators=[NumberRange(0,10)], default=0)
    home_qbr = DecimalField('Home QBR', validators=[NumberRange(0,159)], default=0)

    away_passing_yards = IntegerField('Away Passing Yards', validators=[NumberRange(0,1000)], default=0)
    away_rushing_yards = IntegerField('Away Rushing Yards', validators=[NumberRange(0,1000)], default=0)
    away_turn_overs = IntegerField('Away Turnovers', validators=[NumberRange(0,10)], default=0)
    away_qbr = DecimalField('Away QBR', validators=[NumberRange(0,159)], default=0)

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

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
