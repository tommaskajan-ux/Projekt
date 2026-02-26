from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.models import User, Faculty, Subject, File
from datetime import datetime, timedelta
import re

# Home route - redirects to login page
@app.route('/')
def home():
    return redirect(url_for('login'))


# Login route - handles both showing the form and processing it
@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET request - just show the login page
    if request.method == 'GET':
        return render_template('auth/login.html')

    # POST request - process the login form
    if request.method == 'POST':
        # Get what the user typed in the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if both fields are filled in
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))

        # Find the user in the database by email
        user = User.query.filter_by(email=email).first()

        # If no user found with that email
        if not user:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        # Check if account is disabled
        if not user.is_active:
            flash('Your account has been disabled', 'error')
            return redirect(url_for('login'))

        # Check if account is locked due to too many failed attempts
        if user.is_locked():
            flash('Your account is temporarily locked due to too many failed login attempts', 'error')
            return redirect(url_for('login'))

        # Check if the password matches the hashed password in the database
        # bcrypt.check_password_hash compares plain text password with hashed version
        if not bcrypt.check_password_hash(user.password, password):
            # Increment failed login counter
            user.failed_logins += 1

            # Lock the account after 5 failed attempts for 15 minutes
            if user.failed_logins >= 10:
                user.locked_until = datetime.utcnow() + timedelta(minutes=20)
                db.session.commit()
                flash('Too many failed attempts, your account is locked for 15 minutes', 'error')
                return redirect(url_for('login'))

            db.session.commit()
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        # Update last login time on successful login
        user.last_login = datetime.utcnow()

        # Reset failed login counter on successful login
        user.failed_logins = 0
        user.locked_until = None
        db.session.commit()

        flash('Welcome back ' + user.full_name(), 'success')
        return redirect(url_for('dashboard'))


# Register route - handles both showing the form and processing it
@app.route('/register', methods=['GET', 'POST'])
def register():
    # GET request - just show the register page
    if request.method == 'GET':
        # Pass all active faculties to the form so user can pick one
        faculties = Faculty.query.filter_by(is_active=True).all()
        return render_template('auth/register.html', faculties=faculties)

    # POST request - process the registration form
    if request.method == 'POST':
        # Get what the user typed in the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        faculty_id = request.form.get('faculty_id')

        # Check if all fields are filled in
        if not all([first_name, last_name, username, email, password, faculty_id]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('register'))

        # Check if email is in UTB format - must be d_hlinka@utb.cz
        utb_email_pattern = r'^[a-zA-Z]{1}[_][a-zA-Z]+@utb\.cz$'
        if not re.match(utb_email_pattern, email):
            flash('You must use your UTB email address e.g. d_hlinka@utb.cz', 'error')
            return redirect(url_for('register'))

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('register'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Check if password is long enough
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('register'))

        # Check if password contains at least one number
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number', 'error')
            return redirect(url_for('register'))

        # Check if password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter', 'error')
            return redirect(url_for('register'))

        # Hash the password before saving - NEVER save plain text passwords
        # bcrypt.generate_password_hash takes plain text and returns a secure hash
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create the new user object with the hashed password
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            # Save the hashed version not the plain text
            password=hashed_password,
            faculty_id=faculty_id
        )

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully, please log in', 'success')
        return redirect(url_for('login'))


# Dashboard route - main page after login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')


# Logout route
@app.route('/logout')
def logout():
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))