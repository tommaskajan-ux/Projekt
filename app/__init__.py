# Import Flask class to create the app
from flask import Flask

# Import SQLAlchemy to handle database connection
from flask_sqlalchemy import SQLAlchemy

# Import load_dotenv to read the .env file
from dotenv import load_dotenv

# Import os to access environment variables
import os

# Load all variables from .env file into memory
load_dotenv()

# Create the Flask application instance
# __name__ tells Flask the name of the current module (evaluates to "app")
app = Flask(__name__)

# Set the secret key from .env - used to secure user sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Set the database URL from .env - tells SQLAlchemy where PostgreSQL is running
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Create the database object - this is your gateway to PostgreSQL
# You'll use db.session.add(), db.session.commit() etc. throughout the project
db = SQLAlchemy(app)

# Import routes at the bottom to avoid circular import errors
# (routes.py also imports from this file so it must come last)
from app import routes