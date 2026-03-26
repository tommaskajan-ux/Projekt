from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
import uuid
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Faculty(db.Model):
    __tablename__ = 'faculties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    subjects = db.relationship('Subject', backref='faculty', lazy=True)
    users = db.relationship('User', backref='faculty', lazy=True)

    def __repr__(self):
        return f'<Faculty {self.code}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    files = db.relationship('File', backref='subject', lazy=True)

    def __repr__(self):
        return f'<Subject {self.code}>'


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Changed to False — account locked until email verified
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    failed_logins = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)

    # Links user to their verification tokens
    tokens = db.relationship('VerificationToken', backref='user', lazy=True)

    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User {self.username}>'


class VerificationToken(db.Model):
    __tablename__ = 'verification_tokens'

    id = db.Column(db.Integer, primary_key=True)

    # The token string — uuid hex, impossible to guess
    token = db.Column(db.String(100), unique=True, nullable=False)

    # When this token expires — 24 hours after creation
    expires_at = db.Column(db.DateTime, nullable=False)

    # Whether this token has already been used
    used = db.Column(db.Boolean, default=False, nullable=False)

    # Which user this token belongs to
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Generates a fresh token with 24 hour expiry
    @staticmethod
    def generate(user_id):
        token = VerificationToken(
            token=uuid.uuid4().hex,
            expires_at=datetime.utcnow() + timedelta(hours=24),
            user_id=user_id
        )
        return token

    # Checks if token is still valid — not used AND not expired
    def is_valid(self):
        return not self.used and self.expires_at > datetime.utcnow()


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(500), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    filesize = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

    @staticmethod
    def generate_stored_filename(original_filename):
        ext = os.path.splitext(original_filename)[1]
        return f'{uuid.uuid4().hex}{ext}'

    def __repr__(self):
        return f'<File {self.filename}>'
