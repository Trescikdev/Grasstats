from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_identity = request.form['login_identity']
        password_attempt = request.form['password']
        
        conn = get_db_connection() 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (login_identity, login_identity))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password_attempt):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash("Invalid username/email or password", "danger")
            return redirect(url_for('auth.login'))
            
    return render_template('sign-in.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                           (username, email, hashed_password))            
            conn.commit()

            user_id = cursor.lastrowid

            cursor.execute("INSERT INTO settings (user_id, language) VALUES (?, ?)",
                           (user_id, 'en'))
            conn.commit()
            flash("Account created!", "success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
            return redirect(url_for('auth.register'))
        finally:
            conn.close()
            
    return render_template('sign-up.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))