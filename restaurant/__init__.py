from flask import Flask
from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/anchalsingh/Desktop/restaurant-web-app/restaurant/tables.db'
app.config['SECRET_KEY'] = 'P2ReO53mwBpMi5VwS0QisHjL9tEIMGzU'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #to redirect user to login page if login required

#OTP API
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
api = AuthyApiClient(app.config['AUTHY_API_KEY'])

from restaurant import routes 
