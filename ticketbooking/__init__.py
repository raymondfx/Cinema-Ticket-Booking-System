from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '59904b3ad26ac46eec970dbad8fbff2e'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ticketbooking'
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR_EMAIL'
app.config['MAIL_PASSWORD'] = 'YOUR_PASSWORD'
mail = Mail(app)

from ticketbooking import routes
