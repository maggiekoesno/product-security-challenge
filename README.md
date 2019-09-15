# Zendesk Product Security
### The Zendesk Product Security Challenge

In this repository, there are the following files:
1. README.md - this file
2. _README.md - the original README
3. .gitignore - to ignore certain files when developing
4. main.py - the python program to run to start the project
5. src/ - python files and two other folders
6. src/static - contains css file
7. src/templates - contains html files

## Running the Project
This project was written on Python v3.7.4
---
Make sure to use the pip3 or pip and python3 or python correctly according to your machine.
---
Make sure you have the correct version of Python and install the following packages:
```bash
pip install flask
pip install flask-wtf
pip install flask-sqlalchemy
pip install flask-bcrypt
pip install flask-mail
```
After you have installed all the necessary packages, clone this repository and make sure you are in the "product_security_challenge/" directory and run the following python file:

```bash
python main.py
```
This should run the server. You can then access the application by typing localhost:5000 into your browser.
Google chrome is recommended.

## Features Implemented

# Input sanitization and validation
- Flask provides XSS prevention by using Jinja2 and configuring it so that it has the ability to escape all values unless explicitly set to do otherwise.
- SQLAlchemy is designed in such a way to avoid SQL Injection. It quotes special characters such as semicolons or apostrophes
which means that unless we attempt to bypass their quoting mechanisms, we should be safe from SQL Injection attempts. We can mitigate SQL Injection attacks while using SQLAlchemy by avoiding the use of raw SQL and making use of their framework to interact with our database. 
- Flask's WTForms provides us with validators that takes in the input and verifies it for us based on the criteria we require. By making use of these validators we ensure that the data we are getting is what we expect from the users. 
For example, we use the built-in validator ```wtforms.validators.Email``` to verify if the given string is a valid email address. We also use custom validators to verify the data based on our own requirements. 

# Password hashed
Password is hashed before being stored into the database using the bcrypt module. Bcrypt provides a great hashing algorithm as it always hashes every password with a salt do make cracking a user's password significantly harder and eliminating the possibility of using a hashing table to figure out a user's password.

# Prevention of timing attacks


# Logging
# CSRF prevention
The Flask-WTF extension uses the value of the SECRET_KEY to provide protection for FlaskForms from CSRF attacts. The argument ```{{ form.hidden_tag() }}``` has been placed in each form in the HTML file with the help of Jinja. This argument generates a hidden field that includes a token to help protect the form from CSRF attacks.

# Multi factor authentication
# Password reset / forget password mechanism
If the user wishes to reset their password or have forgotten their password, they can reset the password by clicking on the "Forgot Password" link on the login page. This will redirect them to a form where they can fill in their email address to receive a reset link with a token. Regardless of whether or not the email exists in the database, a flash message will appear for the user to check their email. However, an email will only be sent to said address if a user with that email exists in the database. The user can then reset their password using the link sent to their email that will only be valid for 5 minutes to avoid unwanted use.

# Account lockout

Google Recaptcha v2 is also implemented on all forms to ensure automated requests won't work. This is also implemented to avoid automated brute force attacks.

# Cookie
# HTTPS
  
# Known password check