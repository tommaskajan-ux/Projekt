# Import Flask class to create the app
from flask import Flask

# Import SQLAlchemy to handle database connection
from flask_sqlalchemy import SQLAlchemy

# Import Flask class to create the app
from flask import Flask

# Import SQLAlchemy to handle database connection
from flask_sqlalchemy import SQLAlchemy

# Import Bcrypt for password hashing
from flask_bcrypt import Bcrypt

# Import Minio client for file storage
from minio import Minio

# Import load_dotenv to read the .env file
from dotenv import load_dotenv

# Import os to access environment variables
import os

# Load .env file explicitly from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

print("DATABASE_URL:", os.getenv('DATABASE_URL'))

# Create the Flask application instance
app = Flask(__name__)

# Set the secret key from .env - used to secure user sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Set the database URL from .env - tells SQLAlchemy where PostgreSQL is running
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Disable modification tracking - reduces memory usage
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database object - your gateway to PostgreSQL
db = SQLAlchemy(app)

# Create the bcrypt object - used to hash and verify passwords
bcrypt = Bcrypt(app)

# Create the MinIO client
minio_client = Minio(
    os.getenv('AWS_ENDPOINT_URL').replace('http://', ''),
    access_key=os.getenv('AWS_ACCESS_KEY_ID'),
    secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    secure=False
)

# Import routes at the bottom to avoid circular import errors
from app import routes