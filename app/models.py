from app import db


# User table - stores all registered users
class User(db.Model):
    __tablename__ = 'users'

    # Unique ID for each user, auto increments
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique and cant be empty
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Email must be unique and cant be empty
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Stores the hashed password, never store plain text passwords
    password = db.Column(db.String(200), nullable=False)

    # Automatically saves when the account was created
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # One user can have many files - this links User to File table
    files = db.relationship('File', backref='owner', lazy=True)


# File table - stores metadata about every uploaded document
class File(db.Model):
    __tablename__ = 'files'

    # Unique ID for each file
    id = db.Column(db.Integer, primary_key=True)

    # Original name of the uploaded file
    filename = db.Column(db.String(255), nullable=False)

    # The path/URL where the file is stored in MinIO
    filepath = db.Column(db.String(500), nullable=False)

    # File type e.g. pdf, docx, txt
    filetype = db.Column(db.String(50), nullable=False)

    # Category the user assigns to the file
    category = db.Column(db.String(100), nullable=True)

    # File size in bytes
    filesize = db.Column(db.Integer, nullable=True)

    # When the file was uploaded
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

    # Links this file to a user - every file must belong to someone
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)