from statistics import mean
from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from flask import session
import jwt
import re
import datetime
from flask_migrate import Migrate
import pandas as pd
from .db_config import DB_CONFIG
from .email_config import PASSWORD
import numpy as np
from random import randint
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import csv
import secrets #for forgot password
from flask_mail import Mail, Message
import threading

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"
app = Flask(__name__)
app.secret_key = "test" #for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


app.config['MAIL_SERVER']= 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'EXCHANGE-PLATFORM@hotmail.com'
app.config['MAIL_PASSWORD'] = PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

from .model.transaction import Transaction, transaction_schema, transactions_schema
from .model.user import User, user_schema
from .model.creditcards import CreditCard, credit_card_schema
from .model.usertransaction import UserTransaction, user_transaction_schema, user_transactions_schema
"""
####################################################### Helper Functions ###################################################################
"""
def write_email(subject, recipient, body, sender='usd-lbp-exchange-tracker@hotmail.com'):
    try:
        msg = Message(subject=subject, sender = ("USD-LBP-Exchange-Tracker-Platform", sender), recipients = [recipient])
        msg.body = body
        mail.send(msg)
        return True
    
    except Exception as e:
        return str(e)

def get_all_usd_buy_transactions(start_date,end_date):
    Transactions = Transaction.query.filter(
                                    Transaction.added_date.between(start_date, end_date)
                                    ).all()
    transactions = [t for t in Transactions if t.usd_to_lbp==0]
    return transactions

def get_all_usd_sell_transactions(start_date,end_date):
    Transactions = Transaction.query.filter(
                                    Transaction.added_date.between(start_date, end_date)
                                    ).all()
    transactions = [t for t in Transactions if t.usd_to_lbp==1]
    return transactions

def get_rates_of_a_list(L):
    rates = [t.lbp_amount / t.usd_amount for t in L]
    return rates

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,}$'

    if re.match(email_regex, email):
        return True
    else:
        return False
    
def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY,'HS256')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')
    
def valid_transaction (usd_amount, lbp_amount):
    if(not usd_amount or not lbp_amount or not (isinstance(usd_amount, (int, float)) and isinstance(lbp_amount, (int, float)))
        or usd_amount<=0 or lbp_amount<=0):
        return False
    return True
"""
##################################################### Post a Transaction #################################################################
"""
@app.route('/transaction', methods=['POST'])
def make_transaction():

    try:
        auth_token = extract_auth_token(request)
        
        if not auth_token:
            T = Transaction(
                usd_amount=request.json["usd_amount"],
                lbp_amount=request.json["lbp_amount"],
                usd_to_lbp=request.json["usd_to_lbp"],
                user_id=None  
            )

        else:
            user_id = decode_token(auth_token)
            user_id_exists = User.query.get(user_id)
            if not user_id_exists:
                return jsonify({'success': False, 'message': 'Invalid bearer token. User does not exist.'}), 403
            
            T = Transaction(
                usd_amount=request.json["usd_amount"],
                lbp_amount=request.json["lbp_amount"],
                usd_to_lbp=request.json["usd_to_lbp"],
                user_id=user_id
            )
            if T.usd_to_lbp:
                message = f"Dear {user_id_exists.user_name},\n\nYou added a transaction!\n\nThis transaction consisted of:\n\t- A USD amount equivalent to : {T.usd_amount}\n\t- An LBP amount equivalent to {T.lbp_amount}\n\t- The transaction type was USD to LBP\n\nThank you for using our platform!"
            else:
                message = f"Dear {user_id_exists.user_name},\n\nYou added a transaction!\n\nThis transaction consisted of:\n\t- A USD amount equivalent to : {T.usd_amount}\n\t- An LBP amount equivalent to {T.lbp_amount}\n\t- The transaction type was LBP to USD\n\nThank you for using our platform!"
            write_email('Transaction Recorded Successfuly!',user_id_exists.email,message)

        if valid_transaction(T.usd_amount,T.lbp_amount):
            db.session.add(T)
            db.session.commit()
            serialized_transaction = transaction_schema.dump(T)
            return jsonify(serialized_transaction), 201
        else:
            return jsonify({'success': False, 'message': 'Both the LBP and USD amounts should be filled with values bigger than zero to have a valid transaction'}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
################################################### Fetch Transaction History #################################################################
"""
@app.route('/transaction', methods=['GET'])
def get_user_transactions():
    try:
        auth_token = extract_auth_token(request)
        
        if not auth_token:
            return jsonify({'success': False, 'message': 'Empty Bearer token'}), 403 

        try:
            user_id = decode_token(auth_token)
        except :
            return jsonify({'success': False, 'message': 'User ID does not exist'}), 403 

       
        user_transactions = Transaction.query.filter_by(user_id=user_id).all()
        serialized_transactions = transactions_schema.dump(user_transactions)

        return jsonify(serialized_transactions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
##################################################### Fetch Exchange Rate #################################################################
""" 
def calculate_exchange_rate():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=3)

    transactions_within_window = Transaction.query.filter(
        Transaction.added_date.between(start_date, end_date)
    ).all()

    usd_transactions_sell = [t for t in transactions_within_window if t.usd_to_lbp]
    usd_transactions_buy = [t for t in transactions_within_window if not t.usd_to_lbp]

    usd_sell_rates = get_rates_of_a_list(usd_transactions_sell)
    usd_buy_rates = get_rates_of_a_list(usd_transactions_buy)

    usd_rate_sell = sum(usd_sell_rates) / len(usd_sell_rates) if usd_sell_rates else None
    usd_rate_buy = sum(usd_buy_rates) / len(usd_buy_rates) if usd_buy_rates else None

    return usd_rate_sell, usd_rate_buy

@app.route('/fetch-exchange-rate', methods=['GET'])
def exchange_rate():
    try:
        usd_rate, lbp_rate = calculate_exchange_rate()
        return jsonify({"usd_to_lbp": usd_rate, "lbp_to_usd": lbp_rate}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
######################################################## Create a User #####################################################################
"""

@app.route('/create-user', methods=['POST'])
def create_user():
    try:
        user_name = request.json["user_name"]
        password = request.json["password"]
        email = request.json["email"]

        if not user_name.strip():
            return jsonify({'success': False, 'message': 'Username cannot be empty.'}), 400

        if ' ' in user_name :
            return jsonify({'success': False, 'message': 'Usernames cannot have spaces'}), 400
        
        
        already_existing = User.query.filter_by(user_name=user_name).first()
        if already_existing:
            return jsonify({'success': False, 'message': 'This username is already taken please try again with a different one'}), 400
        
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Enter a valid gmail address'}), 400
        
        already_existing = User.query.filter_by(email=email).first()
        if already_existing:
            return jsonify({'success': False, 'message': 'This email is already taken please try again with a different one'}), 400
        
        if ' ' in password:
            return jsonify({'success': False, 'message': 'Passwords cannot have spaces'}), 400
        
        message = f"Dear {user_name},\n\nWelcome to the Exchange Center!\n\nThis is an automated email, make sure to enjoy our services.\n\nThank you for using our platform!"
        write_email('Welcome to the Exchange Platform',email,message)

        new_user = User(user_name=user_name, password=password, email = email)
        db.session.add(new_user)
        db.session.commit()
        serialized_user = user_schema.dump(new_user)
        return jsonify(serialized_user), 201
        
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
####################################################### Authentication #####################################################################
"""
@app.route('/authentication', methods=['POST'])
def authenticate_user():
    try:
        user_name = request.json["user_name"]
        password = request.json["password"]
        
        if not user_name or not password:
            return jsonify({'success': False, 'message': 'Fill the username and password.'}), 400  

        uuser = User.query.filter_by(user_name=user_name).first()
        
        if not uuser:
            return jsonify({'success': False, 'message': "Username doesn't exist."}), 400

        
        if not bcrypt.check_password_hash(uuser.hashed_password, password):
            
            return jsonify({'success': False, 'message': "Wrong password."}), 400 

        
        token = create_token(uuser.id)
        return jsonify({'token': token}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
####################################################### Statistics ########################################################################
"""   
@app.route('/statistics/min-max-rates', methods=['GET'])
def MinMaxRates():
    try:
        if "start date" and "end date" in session:
            start_date = session["start date"]
            end_date = session["end date"]
        else:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=14)

        usd_buy_transactions = get_all_usd_buy_transactions(start_date,end_date)
        rates = get_rates_of_a_list(usd_buy_transactions)

        max_usd_buy_rate = None
        max_usd_buy_date = None
        min_usd_buy_rate = None
        min_usd_buy_date = None

        for i in range (len(rates)):
            if max_usd_buy_rate is None or rates[i] > max_usd_buy_rate:
                max_usd_buy_rate = rates[i]
                max_usd_buy_date = usd_buy_transactions[i].added_date

            if min_usd_buy_rate is None or rates[i] < min_usd_buy_rate:
                min_usd_buy_rate = rates[i]
                min_usd_buy_date = usd_buy_transactions[i].added_date

        usd_sell_transactions = get_all_usd_sell_transactions(start_date,end_date)
        rates = get_rates_of_a_list(usd_sell_transactions)
        max_usd_sell_rate = None
        max_usd_sell_date = None
        min_usd_sell_rate = None
        min_usd_sell_date = None

        for i in range (len(rates)):
            if max_usd_sell_rate is None or rates[i] > max_usd_sell_rate:
                max_usd_sell_rate = rates[i]
                max_usd_sell_date = usd_sell_transactions[i].added_date

            if min_usd_sell_rate is None or rates[i] < min_usd_sell_rate:
                min_usd_sell_rate = rates[i]
                min_usd_sell_date = usd_sell_transactions[i].added_date

        
        return jsonify({"max_usd_buy_rate": max_usd_buy_rate, 
                       "max_usd_buy_rate_date":max_usd_buy_date,
                       "max_usd_sell_rate": max_usd_sell_rate,
                       "max_usd_sell_rate_date":max_usd_sell_date,
                       "min_usd_buy_rate": min_usd_buy_rate,
                       "min_usd_buy_rate_date": min_usd_buy_date,
                       "min_usd_sell_rate": min_usd_sell_rate,
                       "min_usd_sell_rate_date": min_usd_sell_date}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    
@app.route('/statistics/std-avg', methods=['GET'])
def std():
    try:
        if "start date" and "end date" in session:
            start_date = session["start date"]
            end_date = session["end date"]
        else:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=14)

        usd_buy_std = None
        usd_buy_avg = None
        usd_sell_std= None
        usd_sell_avg = None

        usd_buy_transactions = get_all_usd_buy_transactions(start_date,end_date)
        usd_sell_transactions = get_all_usd_sell_transactions(start_date,end_date)

        usd_buy_rates = get_rates_of_a_list(usd_buy_transactions)
        usd_sell_rates = get_rates_of_a_list(usd_sell_transactions)

        usd_buy_std= np.std(usd_buy_rates)
        usd_sell_std= np.std(usd_sell_rates)
        usd_buy_avg = np.mean(usd_buy_rates)
        usd_sell_avg = np.mean(usd_sell_rates)

        return jsonify({
            "usd_buy_rate_standard_deviation": usd_buy_std,
            "usd_sell_rate_standard_deviation": usd_sell_std,
            "usd_buy_rate_average": usd_buy_avg,
            "usd_sell_rate_average": usd_sell_avg
            }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
     
@app.route('/statistics/total-amount-exchanged', methods=['GET'])
def Total_Amount_Exchanged():
    try:
        if "start date" and "end date" in session:
            start_date = session["start date"]
            end_date = session["end date"]
        else:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=14)
        
        usd_total = None
        lbp_total = None

        usd_buy_transactions = get_all_usd_buy_transactions(start_date,end_date)
        usd_sell_transactions = get_all_usd_sell_transactions(start_date,end_date)

        usd_total_amount = [t.usd_amount for t in usd_buy_transactions] + [t.usd_amount for t in usd_sell_transactions]
        lbp_total_amount = [t.lbp_amount for t in usd_buy_transactions] + [t.lbp_amount for t in usd_sell_transactions]

        usd_total = np.sum(usd_total_amount)
        lbp_total = np.sum(lbp_total_amount)

        return jsonify({
            "total_usd_amount_exchanged": usd_total,
            "total_lbp_amount_exchanged": lbp_total
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/set-date-range', methods=['POST'])
def set_date_range():
    try:
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]

        if not end_date and not start_date:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=14)
           
        if not end_date:
            end_date = datetime.datetime.now()
             
        if not start_date:
            start_date = end_date - datetime.timedelta(days=14)

        session['start date'] = start_date
        session['end date'] = end_date

        return jsonify({"message": "Date range set successfully."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
##################################################### Fluctuation Graph #################################################################
"""
def remove_duplicate_dates(rates, dates):
    unique_dates = []
    unique_rates = []

    for i in range(len(dates)):
        if i == 0 or dates[i] != dates[i-1]:
            unique_dates.append(dates[i])
            unique_rates.append([rates[i]])  
        else:
            unique_rates[-1].append(rates[i])  

    averaged_rates = [mean(i) for i in unique_rates]
    return averaged_rates, unique_dates

@app.route('/fluctuation-graph', methods=['POST'])
def Graph_Exchange_Rate():  
    try:
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
        Transactions = []

        if not end_date and not start_date:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=14)
           
        if not end_date:
            end_date = datetime.datetime.now()
             
        if not start_date:
            start_date = end_date - datetime.timedelta(days=14)
        
        Transactions = Transaction.query.filter(
                                    Transaction.added_date.between(start_date, end_date)
                                    ).all()
        
        usd_buy_rates = [t.lbp_amount/t.usd_amount for t in Transactions if t.usd_to_lbp == 0]
        usd_buy_dates = [t.added_date.strftime("%Y-%m-%d") for t in Transactions if t.usd_to_lbp == 0 ]
        usd_buy_rates,usd_buy_dates = remove_duplicate_dates(usd_buy_rates,usd_buy_dates)

        usd_sell_rates = [t.lbp_amount/t.usd_amount for t in Transactions if t.usd_to_lbp == 1]
        usd_sell_dates = [t.added_date.strftime("%Y-%m-%d") for t in Transactions if t.usd_to_lbp == 1]
        usd_sell_rates,usd_sell_dates = remove_duplicate_dates(usd_sell_rates,usd_sell_dates)

        return jsonify({"usd_buy_rates":usd_buy_rates,"usd_buy_dates":usd_buy_dates,
                        "usd_sell_rates":usd_sell_rates,"usd_sell_dates":usd_sell_dates,}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400  
"""
##################################################### Machine Learning #################################################################
"""


def make_predictions(date):
    df = pd.read_csv(r'aggregated_exchange_rates2.csv')
    df.index = pd.to_datetime(df['DateTime'], format = '%Y-%m-%d')
    scaler = MinMaxScaler()
    df[['USD to LBP']] = scaler.fit_transform(df[['USD to LBP']])
    #print(df.head())
    file_path = 'dates_to_predict.csv'
    model = load_model('model2.keras')
    
    dates_to_predict = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date = datetime.datetime.strptime(row[0], '%Y-%m-%d')
            dates_to_predict.append(date)
    #print(dates_to_predict)
    end_date = date
    i = dates_to_predict[-1]+datetime.timedelta(days=1)
    while i <= end_date:
        dates_to_predict.append(i)
        i += datetime.timedelta(days=1)

    recursive_predictions = []
    recursive_dates = np.array(dates_to_predict)
    #print(recursive_dates)
    file_path = 'last_window.csv'
    last_window = np.loadtxt(file_path, delimiter=',')
    last_window = last_window.reshape(-1, 1)
    #print(last_window)
    for target_date in recursive_dates:
        next_prediction = model.predict(np.array([last_window[-5:]])).flatten()
        recursive_predictions.append(next_prediction)
        last_window = np.concatenate((last_window,[next_prediction]))
    recursive_predictions = scaler.inverse_transform(recursive_predictions)
    return  recursive_predictions[-1]


@app.route('/predict-rate', methods=['POST'])
def make_prediction():
    try:
        date = request.json["date"]
        
        if not date:
            return jsonify({'success': False, 'message': 'date cannot be empty.'}), 400

        try:
            date_value = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format. Date should be in yyyy-mm-dd format.'}), 400

        if date_value <= datetime.datetime.now():
            return jsonify({'success': False, 'message': "Date must be greater than today's date."}), 400

        if date[4]!="-" or date[7]!="-":
            return jsonify({'success': False, 'message': 'the date should be of form yyyy-mm-dd'}), 400

        if int(date[5:7]) > 12 or int(date[8:10]) > 31:
            return jsonify({'success': False, 'message': 'Please input a valid date.'}), 400
        
        predictions = make_predictions(date)

        return jsonify({"predicted_rate": predictions[-1]}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""
####################################################### Credit Card ###################################################################
"""
def verify_credit_card(card, month, year, cvv):
    if not (card and month and year and cvv):
        return False
    if not(year.isdigit() and len(year)==4):
        return False
    if not (card.isdigit() and len(card) == 16):
        return False
    if not (cvv.isdigit() and len(cvv)==3):
        return False
    
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    month = int(month)
    year = int(year)
    if year < current_year:
        return False
    elif year == current_year and month < current_month:
        return False
    return True

@app.route('/add-credit-card', methods=['POST'])
def add_card():
    try:
        auth_token = extract_auth_token(request) 

        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to add a credit card'}), 400
        
        else:
            user_id = decode_token(auth_token)
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'message': 'Invalid bearer token. User does not exist.'}), 403
            
            card_number = request.json["card_number"]
            month = request.json["month"]
            year =  request.json["year"]
            cvv  = request.json["cvv"]
            
            if not verify_credit_card(card_number, month, year, cvv):
                #makes sure the credit card inserted is valid and in addition is not expired
                return jsonify({"error": "Invalid credit card information"}), 400
            
            credit_card = CreditCard(
                card_number=card_number,
                month=month,
                year=year,
                cvv=cvv,
                user_id=user.id
            )

            db.session.add(credit_card)
            db.session.commit()
            serialized_credit_card = credit_card_schema.dump(credit_card)
            return jsonify(serialized_credit_card), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/add-balance', methods=['POST'])
def add_balance():
    try:
        auth_token = extract_auth_token(request)

        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to add balance'}), 400
        
        amount = request.json["amount"]
        usd_or_lbp = request.json["usd_or_lbp"]

        user_id = decode_token(auth_token)
        user = User.query.get(user_id)

        user_credit_card = CreditCard.query.filter_by(user_id=user_id).first()
        if not user_credit_card:
            return jsonify({'success': False, 'message': 'User should add a credit card before adding balance'}), 400
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        if user_credit_card.year<current_year or (user_credit_card.year==current_year and user_credit_card.month<current_month):
            return jsonify({'success': False, 'message': 'Expired credit card'}), 400
        
        if (type(amount) == int or type(amount) == float) and amount>0:
            if usd_or_lbp == "USD":
                user.usd_balance += amount
            
            if usd_or_lbp == "LBP":
                user.lbp_balance += amount

        else:
            return jsonify({'success': False, 'message': 'Invalid inputs'}), 400
        db.session.commit()
        return jsonify({'success': True, 'message': 'Amount added successfully'}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
"""
################################################## Send Transactions Between Users ###############################################################
"""

def schedule_refund(transaction_id):
    with app.app_context():
        print("Ana fetet bel refund schedule")
        transaction = UserTransaction.query.filter_by(id=transaction_id).first()
        print(transaction.id)

        if transaction.accepted == "pending" :#if still pending meaning it expired
            sender = User.query.get(transaction.sender_id)
            if transaction.usd_amount > 0:
                sender.usd_balance += transaction.usd_amount
            elif transaction.lbp_amount > 0:
                sender.lbp_balance += transaction.lbp_amount

            transaction.accepted = "expired"
            db.session.commit()

            sender_subject = "Money Transfer Status"
            sender_message = f"Hello {sender.user_name},\n\nTransaction ID: {transaction_id} has expired because the recipient didn't accept it in time, thus the amount you sent has been refunded.\n\nThank you for using our services!"
            write_email(sender_subject, sender.email, sender_message)
        return 

 
@app.route('/send-transaction-to-user', methods=['POST'])
def send_to_user():
    try:
        auth_token = extract_auth_token(request)
        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to send money'}), 400
        
        sender_id = decode_token(auth_token)
        sender = User.query.get(sender_id)
        sender_email = sender.email

        if not sender:
            return jsonify({'success': False, 'message': 'User does not exist, invalid bearer token'}), 400

        recipient_email= request.json["email_of_recipient"]
        amount = request.json["amount"]
        usd_or_lbp = request.json["usd_or_lbp"]

        if not recipient_email:
            return jsonify({'success': False, 'message': 'Input the email of the recipient'}), 400
        
        if not amount:
            return jsonify({'success': False, 'message': 'Input the amount of money you want to transfer'}), 400
         
        if not usd_or_lbp:
            return jsonify({'success': False, 'message': 'Input the currency of the transfer'}), 400
        
        recipient = User.query.filter_by(email=recipient_email).first()

        if not recipient:
            return jsonify({'success': False, 'message': 'This User does not exist'}), 400
        
        if usd_or_lbp == "USD" and amount>sender.usd_balance:
            return jsonify({'success': False, 'message': 'You do not have enough USD balance to proceed with the transfer'}), 400
        
        if usd_or_lbp == "LBP" and amount>sender.lbp_balance:
            return jsonify({'success': False, 'message': 'You do not have enough LBP balance to proceed with the transfer'}), 400
        
        transaction_id = randint(0, 999999)  
        while(UserTransaction.query.filter_by(id=transaction_id).first()):
            transaction_id = randint(0, 999999) 

        delay = 30 * 60
        refund_timer = threading.Timer(delay, schedule_refund, args=[transaction_id])
        

        if usd_or_lbp == "USD":
            sender.usd_balance -= amount
            transaction = UserTransaction(
                id = transaction_id,
                sender_id=sender.id,
                recipient_id=recipient.id,
                usd_amount=amount ,
                lbp_amount= 0
            )
            
            sender_subject = "You Have Sent Money!"
            sender_message = f"Hello {sender.user_name},\n\nIt looks like you have sent {amount} USD to {recipient_email}. An email has been sent to the recipient, he has 30 mins to accept the transaction.\n\nThank you for using our services!"
            write_email(sender_subject, sender_email, sender_message)
            
            recipient_subject = "You Received Money!"
            recipient_message = f"Hello {recipient.user_name},\n\nIt looks like you received {amount} USD from {sender_email}. Please copy the following transaction ID: {transaction_id}, open our platform, paste it, and either accept or decline the money.\nYou have 30 mins to do so.\n\nThank you for using our services!"
            write_email(recipient_subject, recipient_email, recipient_message)
            db.session.add(transaction)
            db.session.commit()
            refund_timer.start()
            serialized_transaction = user_transaction_schema.dump(transaction)
            return jsonify(serialized_transaction), 201

        elif usd_or_lbp == "LBP":
            sender.lbp_balance -= amount
            transaction = UserTransaction(
                id = transaction_id,
                sender_id=sender.id,
                recipient_id=recipient.id,
                usd_amount=0,
                lbp_amount= amount
            )
            sender_subject = "You Have Sent Money!"
            sender_message = f"Hello {sender.user_name},\n\nIt looks like you have sent {amount} LBP to {recipient_email}. An email has been sent to the recipient, he has 30 mins to accept the transaction.\n\nThank you for using our services!"
            write_email(sender_subject, sender_email, sender_message)

            recipient_subject = "You Received Money!"
            recipient_message = f"Hello {recipient.user_name},\n\nIt looks like you received {amount} LBP from {sender_email}. Please copy the following transaction ID: {transaction_id}, open our platform, paste it, and either accept or decline the money.\nYou have 30 mins to do so.\n\nThank you for using our services!"
            write_email(recipient_subject, recipient_email, recipient_message)
            db.session.add(transaction)
            db.session.commit()
            refund_timer.start()
            serialized_transaction = user_transaction_schema.dump(transaction)
            return jsonify(serialized_transaction), 201
        else:
            return jsonify({'success': False, 'message': 'Enter either USD or LBP'}), 400

    except Exception as e:
          return jsonify({"error": str(e)}), 400

@app.route('/accept-decline-transaction', methods=['POST'])
def accept_decline_transaction():
    try:
        auth_token = extract_auth_token(request)
        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to accept or decline a transaction'}), 400
        
        user_id = decode_token(auth_token)
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User does not exist, invalid bearer token'}), 400
        
        transaction_id = request.json["transaction_id"]
        accept = request.json["accept"]
        transaction = UserTransaction.query.get(transaction_id)

        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction does not exist'}), 400
        
        if user.id != transaction.recipient_id:
            return jsonify({'success': False, 'message': 'You are not the recipient of this transaction'}), 400
        
        if transaction.accepted == "pending":
            
            sender_id = transaction.sender_id
            sender = User.query.filter_by(id=sender_id).first()
            sender_email = sender.email

            if accept:
                transaction.accepted = "accepted"
                if transaction.usd_amount > 0:
                    user.usd_balance += transaction.usd_amount

                if transaction.lbp_amount > 0:
                    user.lbp_balance += transaction.lbp_amount

                sender_subject = "Money Transfer Status"
                sender_message = f"Hello {sender.user_name},\n\nTransaction ID: {transaction_id} has been accepted by {user.email}.\n\nThank you for using our services!"
                write_email(sender_subject, sender_email, sender_message)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Transaction accepted successfully'}), 200
            else:
                transaction.accepted = "declined"
                sender_subject = "Money Transfer Status"
                sender_message = f"Hello {sender.user_name},\n\nTransaction ID: {transaction_id} was declined by {user.email}, nothing has been deducted from your balance.\n\nThank you for using our services!"
                write_email(sender_subject, sender_email, sender_message)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Transaction declined successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'The transaction was already either accepted or declined'}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
################################################## Forgot Password For Logged out users ###############################################################
"""
def generate_reset_OTP():
    OTP = secrets.token_hex(16)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15) 
    return OTP, expiration_time

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        email = request.json["email"]

        if not email:
            return jsonify({'success': False, 'message': 'Email cannot be empty'}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'message': 'User with this email does not exist.'}), 404
        
        OTP, expiration_time = generate_reset_OTP()

        user.reset_password_OTP = OTP
        user.reset_OTP_expiration = expiration_time
        db.session.commit()
        
        subject = "Password Reset Request"
        link = "http://127.0.0.1:5000/reset-password"
        message = f"Hello {user.user_name},\n\nYou have requested to reset your password. Please copy and paste the One Time Password under this link {link}\n\nOTP: {OTP}\n\nIf you did not request this, please ignore this email."
        
        write_email(subject, email, message)
        return jsonify({'success': True, 'message': 'Password reset email has been sent to the corresponding email address.'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        OTP = request.json["OTP"]
        new_password = request.json["new_password"]
        
        if not new_password:
            return jsonify({'success': False, 'message': 'New password is required.'}), 400

        user = User.query.filter_by(reset_password_OTP=OTP).first()

        if not user or datetime.datetime.utcnow() > user.reset_OTP_expiration:
            return jsonify({'success': False, 'message': 'Invalid or expired token.'}), 400

        user.hashed_password = bcrypt.generate_password_hash(new_password)
        user.reset_password_OTP = None  # Clear the reset password token
        user.reset_OTP_expiration = None
        db.session.commit()

        return jsonify({'success': True, 'message': 'Password has been reset successfully.'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
################################################## Change Password, Change email, Change credit card ###############################################################
"""

@app.route('/change-password', methods=['POST'])
def change_password():
    try:
        auth_token = extract_auth_token(request)
        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to change passwords'}), 400
        
        user_id = decode_token(auth_token)
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User does not exist, invalid bearer token'}), 400
        
        old_password = request.json["old_password"]
        new_password = request.json["new_password"]
        confirm_password = request.json["confirm_password"]

        if not (old_password and new_password and confirm_password):
            return jsonify({'success': False, 'message': 'Please fill all the above'}), 400
        
        if not bcrypt.check_password_hash(user.hashed_password, old_password):
            return jsonify({'success': False, 'message': 'Wrong password, please input correctly your old password'}), 400
        
        if ' ' in new_password:
            return jsonify({'success': False, 'message': 'Passwords cannot contain spaces.'}), 400
        
        if new_password!=confirm_password:
            return jsonify({'success': False, 'message': 'Your confirm password is not equal to your new password'}), 400
        
        user.hashed_password = bcrypt.generate_password_hash(confirm_password)
        db.session.commit()
        subject = "Password Change Request"
        message = f"Hello {user.user_name},\n\nPassword changed successfully!\n\nIf you did not request this, please contact us through our email ASAP!"
        write_email(subject,user.email,message)
        return jsonify({'success': True, 'message': 'Password has been changed successfully!'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/change-email', methods=['POST'])
def change_email():
    try:
        auth_token = extract_auth_token(request)
        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to change email.'}), 400
        
        user_id = decode_token(auth_token)
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User does not exist, invalid bearer token'}), 400
        
        new_email = request.json["new_email"]
        
        if not (new_email):
            return jsonify({'success': False, 'message': 'Please fill in the new email'}), 400
        
        if not is_valid_email(new_email):
            return jsonify({'success': False, 'message': 'Enter a valid gmail address'}), 400

        already_existing = User.query.filter_by(email=new_email).first()
        if already_existing:
            return jsonify({'success': False, 'message': 'This email is already taken please try again with a different one'}), 400
        
        user.email = new_email
        db.session.commit()
        subject = "Change Email"
        message = f"Hello {user.user_name},\n\nIt looks like you changed your email to this one!\n\nEnjoy our services!"
        write_email(subject,new_email,message)
        return jsonify({'success': True, 'message': 'Email has been changed successfully!'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/change-credit-card', methods=['POST'])
def change_credit_card():
    try:
        auth_token = extract_auth_token(request)
        if not auth_token:
            return jsonify({'success': False, 'message': 'User should be logged in in order to change email.'}), 400
        
        user_id = decode_token(auth_token)
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User does not exist, invalid bearer token'}), 400
        
        user_credit_card = CreditCard.query.filter_by(user_id=user.id).first()
        if not user_credit_card:
            return jsonify({'success': False, 'message': 'User should have a credit card before changing one.'}), 400
        

        new_card_number = request.json["new_card_number"]
        new_month = request.json["new_month"]
        new_year =  request.json["new_year"]
        new_cvv  = request.json["new_cvv"]

        if not verify_credit_card(new_card_number,new_month,new_year,new_cvv):
            return jsonify({"error": "Invalid credit card information"}), 400
        
        user_credit_card.card_number=new_card_number
        user_credit_card.month = new_month
        user_credit_card.year = new_year
        user_credit_card.cvv = new_cvv
        
        db.session.commit()
        subject = "Change Credit Card"
        message = f"Hello {user.user_name},\n\nYou have successfully changed your credit card information!\n\nEnjoy our services!"
        write_email(subject,user.email,message)
        return jsonify({'success': True, 'message': 'Credit Card has been changed successfully!'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
##################################################### Display Balance, Email for Profile Sidebar ###############################################################
"""
@app.route('/fetch-balance', methods=['GET'])
def fetch_balance():
    try:
        auth_token = extract_auth_token(request)
        
        if not auth_token:
            return jsonify({'success': False, 'message': 'Empty Bearer token'}), 403 

        try:
            user_id = decode_token(auth_token)
        except :
            return jsonify({'success': False, 'message': 'User ID does not exist'}), 403 

        user = User.query.get(user_id)

        return jsonify({"usd_balance": user.usd_balance, 
                        "lbp_balance":user.lbp_balance}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/fetch-email', methods=['GET'])
def fetch_email():
    try:
        auth_token = extract_auth_token(request)
        
        if not auth_token:
            return jsonify({'success': False, 'message': 'Empty Bearer token'}), 403 

        try:
            user_id = decode_token(auth_token)
        except :
            return jsonify({'success': False, 'message': 'User ID does not exist'}), 403 

        user = User.query.get(user_id)
        email = user.email

        return jsonify({"user_email": email}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":   
    app.run(debug = False)