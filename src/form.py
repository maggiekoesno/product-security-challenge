from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.data_model import Account

class Login(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    otp = StringField(validators=[DataRequired(), Length(6, 6)])
    recaptcha = RecaptchaField()
    log_in = SubmitField('Log In')

class CreateAccount(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=20)])
    confirm_pwd = PasswordField(validators=[DataRequired(), EqualTo('password'), Length(min=8, max=20)])
    recaptcha = RecaptchaField()
    create = SubmitField('Create Account')

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError('This email already has an account. Please login or use a different email!')

    def validate_username(self, username):
        u = username.data
        account = Account.query.filter_by(username=u).first()
        if account:
            raise ValidationError('Oh no! Username has been taken. Please choose another username!')
        elif not(u.isalnum()):
            raise ValidationError('Username can only contain letters and/ numbers')

    def validate_password(self, password):
        p = password.data
        if p.isnumeric():
            raise ValidationError('Password can not contain only number')
        elif p.isalpha():
            raise ValidationError('Password can not contain only letters')
        elif self.username.data in p:
            raise ValidationError('Password is too predictable')
        elif p in self.username.data:
            raise ValidationError('Password is too predictable')
    
    def validate_confirm_pwd(self, confirm_pwd):
        p = confirm_pwd.data
        if p.isnumeric():
            raise ValidationError('Password can not contain only number')
        elif p.isalpha():
            raise ValidationError('Password can not contain only letters')
        elif self.username.data in p:
            raise ValidationError('Password is too predictable')
        elif p in self.username.data:
            raise ValidationError('Password is too predictable')

class PasswordResetReq(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()
    send = SubmitField('Send Password Reset Link')

class PasswordReset(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm_pwd = PasswordField(validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    reset = SubmitField('Reset Password')
