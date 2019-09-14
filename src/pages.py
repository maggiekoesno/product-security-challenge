from flask import render_template, url_for, flash, redirect
from src import app
from src.form import Login, CreateAccount
from src.data_model import Account


@app.route("/", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.username.data == 'zendesk' and form.password.data == 'password':
            flash('Login is successful!', 'info')
            return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('index.html', form=form)


@app.route("/create-account", methods=['GET', 'POST'])
def create_account():
    form = CreateAccount()
    if form.validate_on_submit():
        flash(f'Account created successfully!', 'info')
        return redirect(url_for('login'))
    return render_template('create_account.html', form=form)