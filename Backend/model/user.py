from ..app import db, ma, bcrypt
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    hashed_password = db.Column(db.String(128))
    usd_balance = db.Column(db.Float, default=0.0)
    lbp_balance = db.Column(db.Float, default=0.0)
    reset_password_OTP = db.Column(db.String(32), unique=True)
    reset_OTP_expiration = db.Column(db.DateTime)

    def __init__(self, user_name, email, password, usd_balance=0.0, lbp_balance=0.0):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.usd_balance = usd_balance
        self.lbp_balance = lbp_balance
        self.email = email
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "email", "usd_balance", "lbp_balance", "reset_password_OTP", "reset_OTP_expiration")
        model = User

user_schema = UserSchema()
