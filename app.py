import os
import boto3
from flask import Flask, session, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MinIO / S3 client ──────────────────────────────────────────
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('S3_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
    region_name=os.getenv('S3_REGION')
)

# ── Models ─────────────────────────────────────────────────────
class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))

# ── Routes ─────────────────────────────────────────────────────
@app.route('/register', methods=['POST'])
def register():
    hashed = generate_password_hash(request.form['password'])
    student = Student(
        name=request.form['name'],
        email=request.form['email'],
        password_hash=hashed,
        faculty_id=request.form['faculty_id']
    )
    db.session.add(student)
    db.session.commit()
    return redirect('/login')

@app.route('/login', methods=['POST'])
def login():
    student = Student.query.filter_by(email=request.form['email']).first()
    if student and check_password_hash(student.password_hash, request.form['password']):
        session['student_id'] = student.id
        session['faculty_id'] = student.faculty_id
        return redirect('/dashboard')
    return 'Invalid credentials', 401

@app.route('/post', methods=['POST'])
def post():
    if 'student_id' not in session:
        return redirect('/login')
    if int(request.form['faculty_id']) != session.get('faculty_id'):
        abort(403)
    # save post logic here
    return 'Posted successfully', 200

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ── Init ───────────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
