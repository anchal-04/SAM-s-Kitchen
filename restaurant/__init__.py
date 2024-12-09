from flask import Flask
from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/anchalsingh/Desktop/SAM-s-Kitchen/restaurant/tables.db'
app.config['SECRET_KEY'] = 'P2ReO53mwBpMi5VwS0QisHjL9tEIMGzU'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #to redirect user to login page if login required

#OTP API
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
api = AuthyApiClient(app.config['AUTHY_API_KEY'])


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587  # Usually 587 for TLS
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False  # Use SSL
app.config['MAIL_USERNAME'] = 'kitchensams123@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'ykdbanokllaxcygu'  # Replace with your email password

# Initialize Flask-Mail
mail = Mail(app)


from restaurant import routes 
