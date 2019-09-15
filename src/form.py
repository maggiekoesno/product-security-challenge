from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.data_model import Account

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

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError('This email already has an account. Please login or use a different email!')

    def validate_username(self, username):
        account = Account.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError('Oh no! Username has been taken. Please choose another username!')

class PasswordResetReq(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    send = SubmitField('Send Password Reset Link')

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account is None:
            raise ValidationError('There is no account with that email. You must register first.')

class PasswordReset(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm_pwd = PasswordField(validators=[DataRequired(), EqualTo('password')])
    reset = SubmitField('Reset Password')
