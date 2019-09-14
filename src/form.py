from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Login(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    log_in = SubmitField('Log In')

class CreateAccount(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField(validators=[DataRequired()])
    confirm_pwd = PasswordField(validators=[DataRequired(), EqualTo('password')])
    create = SubmitField('Create Account')