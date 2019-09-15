from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from src import database, login, app
from flask_login import UserMixin

@login.user_loader
def user_loader(user_id):
    return Account.query.get(int(user_id))

class Account(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(15), unique=True, nullable=False)
    email = database.Column(database.String(75), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)

    def get_token(self, expires_in):
        timed_serializer = TimedSerializer(app.config['SECRET_KEY'], expires_in)
        return timed_serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        timed_serializer = TimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = timed_serializer.loads(token)['user_id']
        except:
            return None
        return Account.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

