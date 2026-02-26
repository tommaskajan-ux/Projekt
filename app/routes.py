from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from app.models import User, Faculty, Subject, File
from datetime import datetime, timedelta
import re


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        if not user.is_active:
            flash('Your account has been disabled', 'error')
            return redirect(url_for('login'))

        if user.is_locked():
            flash('Your account is temporarily locked due to too many failed login attempts', 'error')
            return redirect(url_for('login'))

        if not bcrypt.check_password_hash(user.password, password):
            user.failed_logins += 1
            if user.failed_logins >= 10:
                user.locked_until = datetime.utcnow() + timedelta(minutes=20)
                db.session.commit()
                flash('Too many failed attempts, your account is locked for 20 minutes', 'error')
                return redirect(url_for('login'))
            db.session.commit()
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        user.last_login = datetime.utcnow()
        user.failed_logins = 0
        user.locked_until = None
        db.session.commit()

        login_user(user)
        flash('Welcome back ' + user.full_name(), 'success')
        return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        faculties = Faculty.query.filter_by(is_active=True).all()
        return render_template('auth/register.html', faculties=faculties)

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        faculty_id = request.form.get('faculty_id')

        if not all([first_name, last_name, username, email, password, faculty_id]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('register'))

        utb_email_pattern = r'^[a-zA-Z]{1}[_][a-zA-Z]+@utb\.cz$'
        if not re.match(utb_email_pattern, email):
            flash('You must use your UTB email address e.g. d_hlinka@utb.cz', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('register'))

        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number', 'error')
            return redirect(url_for('register'))

        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
            faculty_id=faculty_id
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully, please log in', 'success')
        return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    file_count = len([f for f in current_user.files if f.is_active])
    return render_template('dashboard/index.html', file_count=file_count)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
