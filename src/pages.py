import pyqrcode as pyqrcode
from io import BytesIO
from flask import render_template, url_for, flash, redirect, session
from src import app, database, encrypt, mail
from src.form import Login, CreateAccount, PasswordResetReq, PasswordReset, RequestUnlockEmail
from src.data_model import Account
from flask_login import login_user, current_user, logout_user
from flask_mail import Message

def send_lock_email(account):
    if account.locked:
        token = account.get_token(86400)
        msg = Message('ACCOUNT LOCK OUT', sender='dummy.zendeskchallenge@gmail.com',
                    recipients=[account.email])
        msg.body = f'''You have been locked out of your account due to security issues. Please click this link to unlock your account:
    {url_for('unlock_account', token=token, _external=True)}

    The link above will expire in 24 hours. If you missed this email, please click the link below to request a new valid link:
    {url_for('request_unlock_email', _external=True)}
    '''
        mail.send(msg)

def count_failed_attempts(account):
    account.failed_attempts = account.failed_attempts + 1
    if account.failed_attempts > 2:
        account.locked = True
    database.session.commit()

    if account.locked:
        flash('Too many unsuccessful login attempts! You have been locked out of your account, please check your email to unlock your account.', 'danger')
        send_lock_email(account)
        return redirect(url_for('login'))

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('logged_in'))
    form = Login()
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data.lower()).first()
        if account.locked:
            flash('Your account has been locked! Please check your email to unlock your account', 'warning')
            return redirect(url_for('login'))
        if account and encrypt.check_password_hash(account.password, form.password.data):
            if not account.verify_totp(form.otp.data):
                count_failed_attempts(account)
                flash('Invalid OTP', 'danger')
                return redirect(url_for('login'))
            login_user(account, remember=form.remember_me.data)
            return redirect(url_for('logged_in'))
        else:
            count_failed_attempts(account)
            flash('Invalid username or password', 'danger')
    return render_template('index.html', form=form)

@app.route('/unlock-account/<token>', methods = ['GET'])
def unlock_account(token):
    account = Account.verify_token(token)
    if account is None:
        flash('Your link has expired or is invalid! Check the previous email on how to get a new link', 'danger')
        return redirect(url_for('login'))
    account.locked = False
    account.failed_attempts = 0
    database.session.commit()
    return render_template('unlock_account.html')

@app.route('/request-unlock-email', methods = ['GET', 'POST'])
def request_unlock_email():
    form = RequestUnlockEmail()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data.lower()).first()
        if account:
            send_lock_email(account)
        flash('Link has been sent to your email. It will expire in 24 hours.', 'info')
        return redirect(url_for('login'))
    return render_template('request_unlock_email.html', form=form)

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
        account = Account(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_pwd)
        account.set_otp_secret()
        database.session.add(account)
        database.session.commit()
        session['username'] = account.username
        return redirect(url_for('totp'))
    return render_template('create_account.html', form=form)

@app.route('/totp')
def totp():
    if 'username' not in session:
        return redirect(url_for('login'))
    account = Account.query.filter_by(username=session['username']).first()
    if account is None:
        return redirect(url_for('login'))
    return render_template('totp.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    account = Account.query.filter_by(username=session['username']).first()
    if account is None:
        abort(404)
    del session['username']
    url = pyqrcode.create(account.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

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
        account = Account.query.filter_by(email=form.email.data.lower()).first()
        if account:
            send_reset_email(account)
        flash('Please reset your password through the link sent to your email address immediately! Link will expire in 5 mintues', 'info')
        return redirect(url_for('login'))
    return render_template('reset_pwd_req.html', form=form)


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_pwd(token):
    account = Account.verify_token(token)
    if account is None:
        flash('Your link has expired or is invalid! Enter your email to receive a new valid link', 'danger')
        return redirect(url_for('reset_request'))
    form = PasswordReset()
    if form.validate_on_submit():
        hashed_pwd = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        account.password = hashed_pwd
        database.session.commit()
        flash('Password successfully changed!', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)