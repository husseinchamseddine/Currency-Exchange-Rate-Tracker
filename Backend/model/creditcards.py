from ..app import db, ma

class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, card_number, month, year, cvv, user_id):
        self.card_number = card_number
        self.month = month
        self.year = year
        self.cvv = cvv
        self.user_id = user_id

class CreditCardSchema(ma.Schema):
    class Meta:
        fields = ("id", "card_number", "month", "year", "cvv", "user_id")
        model = CreditCard
        
credit_card_schema = CreditCardSchema()