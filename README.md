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
pip install onetimepass
pip instal; pyqrcode
pip install safe
```
After you have installed all the necessary packages, clone this repository and make sure you are in the "product_security_challenge/" directory and run the following python file:

```bash
python main.py
```
This should run the server. You can then access the application by typing localhost:5000 into your browser.
Google chrome is recommended.

## How to use TOTP
You will need to download a mobile application for this feature. There are several applications that can be used such as "FreeOTP Authenticator" or "Google Authenticator". Upon account creation you will presented with a QR Code to scan. This will register your account and share the mutual key in the application. The application will then be able to provide you a TOTP regenerated every 30 seconds for login purposes. Please enter said TOTP everytime you need to login.

## Features Implemented

# Input sanitization and validation
- Flask provides XSS prevention by using Jinja2 and configuring it so that it has the ability to escape all values unless explicitly set to do otherwise.
- SQLAlchemy is designed in such a way to avoid SQL Injection. It quotes special characters such as semicolons or apostrophes
which means that unless we attempt to bypass their quoting mechanisms, we should be safe from SQL Injection attempts. We can mitigate SQL Injection attacks while using SQLAlchemy by avoiding the use of raw SQL and making use of their framework to interact with our database. 
- Flask's WTForms provides us with validators that takes in the input and verifies it for us based on the criteria we require. By making use of these validators we ensure that the data we are getting is what we expect from the users. 
For example, we use the built-in validator ```wtforms.validators.Email``` to verify if the given string is a valid email address. We also use custom validators to verify the data based on our own requirements. 

# Password hashed
Password is hashed before being stored into the database using the bcrypt module. Bcrypt provides a great hashing algorithm as it always hashes every password with a salt do make cracking a user's password significantly harder and eliminating the possibility of using a hashing table to figure out a user's password.

# Logging


# CSRF prevention
The Flask-WTF extension uses the value of the SECRET_KEY to provide protection for FlaskForms from CSRF attacts. The argument ```{{ form.hidden_tag() }}``` has been placed in each form in the HTML file with the help of Jinja. This argument generates a hidden field that includes a token to help protect the form from CSRF attacks.

# Multi factor authentication
Multi factor authentication is implemented with onetimepass library. User will need to download a token generator app which will scan a given QR Code during registration. This will register the shared secret and account information on the user's phone in order to generate a TOTP everytime the user wishes to log in. The TOTP will last 30 seconds every time it is generated.

# Password reset / forget password mechanism
If the user wishes to reset their password or have forgotten their password, they can reset the password by clicking on the "Forgot Password" link on the login page. This will redirect them to a form where they can fill in their email address to receive a reset link with a token. Regardless of whether or not the email exists in the database, a flash message will appear for the user to check their email. However, an email will only be sent to said address if a user with that email exists in the database. The user can then reset their password using the link sent to their email that will only be valid for 5 minutes to avoid unwanted use.

# Account lockout
Google Recaptcha v2 is also implemented on all forms to ensure automated requests won't work. This is also implemented to avoid automated brute force attacks.

# Known password check
This is implemented by using the python package 'safe'. As quoted from their website, safe will check the password for the following criterias:
- Safe will check if the password has a simple pattern, for instance:
    password is in the order on your QWERT keyboards.
    password is simple alphabet step by step, such as: abcd, 1357
- Safe will check if the password is a common used password. Many thanks to Mark Burnett for the great work on 10000 Top Passwords.
- Safe will check if the password has mixed number, alphabet, marks.

To ensure for a better password, password is also checked if it is a substring of the username or contains a substring that is the username.

## Additional note
This error might be encountered on a macbook: 
```urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)>```
To solve this please go to Applications > Python3.7 folder > double click on "Install Certificates.command" file.