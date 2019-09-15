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

## Features Implemented

1. Input sanitization and validation
2. Password hashed
3. Prevention of timing attacks
4. Logging
5. CSRF prevention
6. Multi factor authentication
7. Password reset / forget password mechanism
8. Account lockout
9. Cookie
10. HTTPS
11. Known password check