from src import database, login
from flask_login import UserMixin

class Account(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(15), unique=True, nullable=False)
    email = database.Column(database.String(75), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login.user_loader
def user_loader(user_id):
    return Account.query.get(int(user_id))