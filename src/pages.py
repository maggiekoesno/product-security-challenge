from flask import render_template, url_for, flash, redirect
from src import app, database, encrypt, mail
from src.form import Login, CreateAccount, PasswordResetReq, PasswordReset
from src.data_model import Account
from flask_login import login_user, current_user, logout_user
from flask_mail import Message

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('logged_in'))
    form = Login()
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        if account and encrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember_me.data)
            return redirect(url_for('logged_in'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('index.html', form=form)

@app.route('/logged-in', methods = ['GET'])
def logged_in():
    if current_user.is_authenticated:
        return render_template('info.html')
    else:
        flash('You are not logged in', 'warning')
        return redirect(url_for('login'))

@app.route('/logout', methods = ['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return render_template('info.html')
    else:
        flash('You are not logged in', 'warning')
        return redirect(url_for('login'))

@app.route("/create-account", methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return redirect(url_for('logged_in'))
    form = CreateAccount()
    if form.validate_on_submit():
        hashed_pwd = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        account = Account(username=form.username.data, email=form.email.data, password=hashed_pwd)
        database.session.add(account)
        database.session.commit()
        flash('Account created! Please verify your email before logging in.', 'info')
        return redirect(url_for('login'))
    return render_template('create_account.html', form=form)

def send_reset_email(account):
    token = account.get_token(300)
    msg = Message('Password Reset for Zendesk Product Security Challenge', sender='dummy.zendeskchallenge@gmail.com',
                  recipients=[account.email])
    msg.body = f'''Please click on this link to reset your password:
{url_for('reset_pwd', token=token, _external=True)}

You can ignore this email if you did not request to reset your password.
'''
    mail.send(msg)


@app.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('Please logout first if you want to reset your password then click \'Forgot Password\' on the login screen', 'warning')
        return redirect(url_for('logged_in'))
    form = PasswordResetReq()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        if account:
            send_reset_email(account)
        flash('Please reset your password through the link sent to your email address immediately! Link will expire in 5 mintues', 'info')
        return redirect(url_for('login'))
    return render_template('reset_pwd_req.html', form=form)


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_pwd(token):
    account = Account.verify_token(token)
    if account is None:
        flash('Your link has expired of is invalid! Enter your email to receive a new valid link', 'danger')
        return redirect(url_for('reset_request'))
    form = PasswordReset()
    if form.validate_on_submit():
        hashed_pwd = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        account.password = hashed_pwd
        database.session.commit()
        flash('Password successfully changed!', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)