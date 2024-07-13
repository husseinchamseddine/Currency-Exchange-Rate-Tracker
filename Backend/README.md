# Project Name: Currency Exchange Platform

## Overview
This project is a currency exchange platform where users can register, log in, and perform various transactions related to buying and selling USD. The platform also provides features such as transaction history, statistical analysis of exchange rates, USD to LBP rate prediction using a Recurrent Neural Network (RNN), and a credit card system for adding balance and transferring money between users.

## Features
- **User Authentication:** Users can register and log in to the platform securely.
- **Transaction Posting:** Both logged-in and non-logged-in users can post transactions for buying or selling USD.
- **Exchange Rate Calculation:** Exchange rates are calculated based on a three-day time period.
- **Transaction History:** Logged-in users can view their transaction history.
- **Transaction Fluctuation Graph:** A graph that displays the fluctuation of the rates based on a time period that the user inputs. If left empty the graph displays the fluctuations based on a two week interval
- **Statistical Analysis:** Users can view statistical metrics such as mean, standard deviation, maximum, and minimum rates achieved, along with the corresponding dates, based on a time period he chooses. If left empty these value will be calculated based on two week interval.
- **USD to LBP Rate Prediction:** The platform offers USD to LBP rate prediction using a trained RNN model.
- **Credit Card System:** Users can add credit cards and add balance (USD or LBP) to their accounts.
- **Money Transfer:** Users can send money transfers to each other, and recipients have 30 minutes to accept or decline the transaction.
- **Profile Management:** Users can change their email, password, and credit card details. Forgot password functionality is also available.

## Technologies Used

- **Flask**: Flask is a web framework for Python that I used to build the backend of this project.
- **SMTP**: Simple Mail Transfer Protocol (SMTP) was used for sending email notifications to users.
- **Threading**: Threading was utilized to perform background tasks, such as scheduling refunds and other asynchronous operations.
- **Pandas**: Pandas is a powerful data manipulation library in Python, which I used for processing and analyzing Lebanon's Black Market rate data.
- **tensorflow**: I leveraged tensorflow, a machine learning library , for training and deploying a recurrent neural network (RNN) model to predict USD to LBP exchange rates.
- **bcrypt**: Bcrypt was used for hashing and salting user passwords to enhance security.
- **Flask SQLAlchemy**: Flask SQLAlchemy to manipulate the database in Flask applications.


## Installation
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up the database by running migrations (`flask db upgrade`).

## Usage
1. Register and log in to the platform.
2. Navigate to the relevant sections to perform transactions, view transaction history, and manage profile settings.
3. Use the statistical analysis and rate prediction features as needed.
4. Ensure to add credit cards and maintain a valid balance for money transfers.

## License
This project is licensed under the MIT License.

## Contact
For inquiries or support, please contact [afd08@mail.aub.edu](mailto:afd08@mail.aub.edu).

