from flask import render_template, url_for, flash, redirect
from src import app, database, encrypt
from src.form import Login, CreateAccount
from src.data_model import Account
from flask_login import login_user, current_user, logout_user

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('logged_in'))
    form = Login()
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        if account and encrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember_me.data)
            redirect(url_for('logged_in'))
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