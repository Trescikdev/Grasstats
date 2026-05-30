from flask import Blueprint, request, redirect, url_for, session, flash
from database import get_db_connection

invites_bp = Blueprint("invites", __name__)

@invites_bp.route('/team/invite', methods=['POST'])
def invite_player():
    sender_id = session.get('user_id')
    if not sender_id:
        return redirect(url_for('auth.login'))

    team_id = request.form.get('team_id')
    target_username = request.form.get('username')

    if not sender_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        permission_pass = cursor.execute('SELECT contact_person, contact_person_2 FROM teams WHERE team_id = ?', (team_id,)).fetchone()
        if not (permission_pass['contact_person'] == sender_id or permission_pass['contact_person2'] == sender_id):
            flash('You don\'t have permissions to invite a player into this team', 'danger')
            return redirect(url_for('teams.my_team'))

        user = cursor.execute('SELECT id FROM users WHERE username = ?', (target_username,)).fetchone()
        
        if not user:
            flash('Player not found!', 'danger')
            return redirect(url_for('teams.my_team'))

        receiver_id = user[0]

        member_id = cursor.execute('SELECT m.member_id FROM members m LEFT JOIN users u ON u.id = m.user_id WHERE u.id = ?', (receiver_id,)).fetchone()
        already_in_roster = cursor.execute('SELECT * FROM rosters WHERE player_id = ? AND team_id = ?', (member_id['member_id'], team_id,)).fetchone()
        if already_in_roster:
            flash('Player already in your roster!', 'danger')
            return redirect(url_for('teams.my_team'))

        existing = cursor.execute('''
            SELECT 1 FROM invitations 
            WHERE team_id = ? AND receiver_id = ? AND status = 'pending'
        ''', (team_id, receiver_id)).fetchone()

        if not existing:
            cursor.execute('''
                INSERT INTO invitations (team_id, sender_id, receiver_id)
                VALUES (?, ?, ?)
            ''', (team_id, sender_id, receiver_id))
            conn.commit()

    finally:
        conn.close()

    flash("Player invited!", "success")
    return redirect(url_for('teams.my_team'))

@invites_bp.route('/invite/<int:id>/<action>')
def handle_invite(id, action):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        if action == 'accept':
            invite = cursor.execute('SELECT team_id FROM invitations WHERE invitation_id = ?', (id,)).fetchone()
            cursor.execute('INSERT INTO rosters (team_id, player_id) VALUES (?, ?)', (invite[0], user_id))
            cursor.execute('UPDATE invitations SET status = "accepted" WHERE invitation_id = ?', (id,))

        else:
            cursor.execute('UPDATE invitations SET status = "declined" WHERE invitation_id = ?', (id,))

        conn.commit()
    finally:
        conn.close()
    
    return redirect(url_for('profile.my_profile'))
