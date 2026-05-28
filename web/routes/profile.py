from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from database import get_db_connection
from werkzeug.utils import secure_filename
import os

profile_bp = Blueprint('profile', __name__)


def data_processing(sql_record):
    data = []
    for rec in range(1, len(sql_record)):
        data.append(sql_record[rec])

    data[0] = '#{}'.format(data[0])
    translate = {'D' : 'Defense', 'C' : 'Center', 'F' : 'Forward', 'GK' : 'Goalkeeper', None : ''}
    data[1] = translate[data[1]]
    if data[2] == 0:
        data[2] = 'Right handed (left hand lower)'
    else:
        data[2] = 'Left handed (right hand lower)'
    data[3] = '{} cm'.format(data[3])
    data[4] = '{} kg'.format(data[4])
    return data

@profile_bp.route('/my_profile')
def my_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        user_data = cursor.execute('''
            SELECT u.email, m.* 
            FROM users u 
            LEFT JOIN members m ON u.id = m.user_id
            WHERE u.id = ?
        ''', (user_id,)).fetchone()

        if not user_data:
            flash('User can\'t be found!', 'danger')
            return redirect('teams.my_team')

        invites = cursor.execute('''
            SELECT i.invitation_id as invite_id, t.name as team_name, u.username as sender_name
            FROM invitations i
            JOIN teams t ON i.team_id = t.team_id
            JOIN users u ON i.sender_id = u.id
            WHERE i.receiver_id = ? AND i.status = 'pending'
        ''', (user_id,)).fetchall()

        player_data = cursor.execute('''
            SELECT *
            FROM players
            WHERE member_id = ?
        ''', (user_data[1],)).fetchone()

        if player_data:
            player_data = data_processing(player_data)
    finally:
        conn.close()

    return render_template('my_profile.html', user=user_data, invites=invites, player=player_data)

def file_handling(user_id, file):
    filename = secure_filename(file.filename)
    unique_filename = f"user_{user_id}_{filename}"

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
    return unique_filename

@profile_bp.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        if request.method == 'POST':
            full_name = request.form.get('full_name')
            nickname = request.form.get('nickname')
            dob = request.form.get('dob')
            role = request.form.get('role')

            jersey_number = request.form.get('jersey')
            position = request.form.get('position')
            left_handed = 0 if request.form.get('checkboxlefthanded') else 1
            height = request.form.get('height')
            weight = request.form.get('weight')
            szfb_link = request.form.get('szfb_link')

            cursor.execute("SELECT 1 FROM members WHERE user_id = ?", (user_id,))
            exists = cursor.fetchone()

            file = request.files.get('profile_pic')
            photo_filename = None
            if file and file.filename != '':
                photo_filename = file_handling(user_id, file)

            if exists:
                if not photo_filename:
                    cursor.execute('''
                        UPDATE members 
                        SET full_name = ?, nickname = ?, date_of_birth = ?, role = ?
                        WHERE user_id = ?
                    ''', (full_name, nickname, dob, role, user_id))    
                else:
                    cursor.execute('''
                        UPDATE members 
                        SET full_name = ?, nickname = ?, date_of_birth = ?, role = ?, photo = ?
                        WHERE user_id = ?
                    ''', (full_name, nickname, dob, role, photo_filename, user_id))

                member_id = cursor.execute('''SELECT m.member_id FROM users u JOIN members m ON m.user_id = u.id WHERE u.id = ?''', (user_id,)).fetchone()

                cursor.execute('''
                    UPDATE players
                    SET jersey_number = ?, position = ?, left_handed = ?, height_cm = ?, weight_kg = ?, szfb_link = ?
                    WHERE member_id = ?
                ''', (jersey_number, position, left_handed, height, weight, szfb_link, member_id['member_id']))
            else:
                cursor.execute('''
                    INSERT INTO members (user_id, full_name, nickname, date_of_birth, role, photo) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, full_name, nickname, dob, role, photo_filename))
                cursor.execute('''
                    INSERT INTO players (jersey_number, position, left_handed, height_cm, weight_kg, szfb_link)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (jersey_number, position, left_handed, height, weight, szfb_link))

            conn.commit()
            conn.close()
            flash("Profile updated!", "success")
            return redirect(url_for('profile.my_profile'))

        user_data = cursor.execute('''
            SELECT u.email, m.full_name, m.nickname, m.date_of_birth, m.role, m.photo, m.member_id
            FROM users u 
            LEFT JOIN members m ON u.id = m.user_id 
            WHERE u.id = ?
        ''', (user_id,)).fetchone()

        player_data = cursor.execute('''
            SELECT * 
            FROM players p
            JOIN members m ON m.member_id = p.member_id
            WHERE m.member_id = ?
        ''', (user_data[6],)).fetchone()
    finally:
        conn.close()

    return render_template('profile-edit.html', user=user_data, player = player_data)

@profile_bp.route('/profile/<int:m_id>')
def profile(m_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        user_id = cursor.execute('''SELECT u.id
                                FROM users u LEFT JOIN members m
                                ON u.id = m.user_id
                                WHERE m.member_id = ?
                                ''', (m_id,)).fetchone()

        if not user_id:
            flash('user does not exist', 'danger')
            return render_template('all_players.html')
        
        user_id = user_id['id']

        user_data = cursor.execute('''
            SELECT u.email, m.* 
            FROM users u 
            LEFT JOIN members m ON u.id = m.user_id
            WHERE u.id = ?
        ''', (user_id,)).fetchone()

        player_data = cursor.execute('''
            SELECT *
            FROM players
            WHERE member_id = ?
        ''', (user_data[1],)).fetchone()

        if player_data:
            player_data = data_processing(player_data)

    finally:
        conn.close()
    return render_template('profile.html', user=user_data, player=player_data)
