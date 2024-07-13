from ..app import db, ma
import datetime
class UserTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usd_amount = db.Column(db.Float)
    lbp_amount = db.Column(db.Float)
    accepted = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, sender_id, recipient_id, usd_amount, lbp_amount):
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.usd_amount = usd_amount
        self.lbp_amount = lbp_amount

class UserTransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "sender_id", "recipient_id", "usd_amount", "lbp_amount", "accepted", "created_at")

user_transaction_schema = UserTransactionSchema()
user_transactions_schema = UserTransactionSchema(many=True)