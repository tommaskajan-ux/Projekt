from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  # ADD THIS
from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)          # ADD THIS
login_manager.login_view = 'login'         # ADD THIS — matches your @app.route('/login') function name
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'error'  # ADD THIS — uses your existing red flash style

minio_client = Minio(
    os.getenv('AWS_ENDPOINT_URL').replace('http://', ''),
    access_key=os.getenv('AWS_ACCESS_KEY_ID'),
    secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    secure=False
)

from app import routes
