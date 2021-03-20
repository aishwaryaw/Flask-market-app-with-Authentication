from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder = 'templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
app.config['SECRET_KEY'] = '7e77deaf05116196b04e1eb2'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes