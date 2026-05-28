from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from database import get_db_connection

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        
    finally:
        conn.close()

    return render_template('settings.html')

def get_user_language(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        row = cursor.execute('SELECT language FROM settings WHERE user_id = ?', (user_id,)).fetchone()
    finally:
        conn.close()
    return row['language'] if row else None

def save_user_language(user_id, language):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM settings WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute('UPDATE settings SET language = ? WHERE user_id = ?', (language, user_id))
        else:
            cursor.execute('INSERT INTO settings (user_id, language) VALUES (?, ?)', (user_id, language))
            
        conn.commit()
    finally:
        conn.close()

@settings_bp.route('/api/save-language', methods=['POST'])
def api_save_language():
    user_id = session.get('user_id') 
    if not user_id:
        return jsonify({"status": "ignored"}), 200
        
    data = request.get_json()
    language = data.get('language')
    
    if language in ['en', 'sk']:
        save_user_language(user_id, language)
        return jsonify({"status": "success"}), 200
        
    return jsonify({"status": "error"}), 400