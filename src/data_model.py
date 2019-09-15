import os
import base64
import onetimepass
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
    locked = database.Column(database.Boolean, default=False, nullable=False)
    failed_attempts = database.Column(database.Integer, default = 0)
    otp_secret = database.Column(database.String(16))

    def set_otp_secret(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

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

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)