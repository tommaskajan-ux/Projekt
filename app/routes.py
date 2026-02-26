from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user  # ADD THIS
from app import app, db, bcrypt
from app.models import User, Faculty, Subject, File
from datetime import datetime, timedelta
import re


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:          # ADD THIS — bounce logged-in users away
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

        # Reset counters BEFORE login_user()
        user.last_login = datetime.utcnow()
        user.failed_logins = 0
        user.locked_until = None
        db.session.commit()

        login_user(user)                        # ADD THIS — creates the session cookie
        flash('Welcome back ' + user.full_name(), 'success')
        return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:          # ADD THIS — bounce logged-in users away
        return redirect(url_for('dashboard'))

    # ... rest of register unchanged ...


@app.route('/dashboard')
@login_required                                # ADD THIS — blocks unauthenticated access
def dashboard():
    return render_template('dashboard/index.html')


@app.route('/logout')
@login_required                                # ADD THIS — prevents hitting logout when already logged out
def logout():
    logout_user()                              # ADD THIS — clears the session cookie
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
