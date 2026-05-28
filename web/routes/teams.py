from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from database import get_db_connection
from werkzeug.utils import secure_filename
from functions import get_roster_data
import os

teams_bp = Blueprint('teams', __name__)


@teams_bp.route('/my_team', methods=['GET', 'POST'])
def my_team():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        facilities_data = cursor.execute("SELECT * from facilities").fetchall()

        teams = cursor.execute('''
            SELECT DISTINCT 
                t.*, 
                f.name AS facility_name,
                
                next_m.match_id AS next_match_id,
                next_m.date_time AS next_match_date,
                (SELECT name FROM facilities WHERE facility_id = next_m.facility) AS next_match_facility_name,
                (SELECT name FROM teams WHERE team_id = CASE WHEN next_m.home_team = t.team_id THEN next_m.away_team ELSE next_m.home_team END) AS next_opponent_name,
                
                last_m.match_id AS last_match_id,
                last_m.date_time AS last_match_date,
                (SELECT name FROM facilities WHERE facility_id = last_m.facility) AS last_match_facility_name,
                (SELECT name FROM teams WHERE team_id = CASE WHEN last_m.home_team = t.team_id THEN last_m.away_team ELSE last_m.home_team END) AS last_opponent_name

            FROM teams t
            LEFT JOIN facilities f ON t.location = f.facility_id
            LEFT JOIN rosters r ON t.team_id = r.team_id
            
            LEFT JOIN matches next_m ON next_m.match_id = (
                SELECT match_id FROM matches 
                WHERE (match_keeper = t.team_id)
                AND datetime(date_time) >= datetime('now', 'localtime')
                ORDER BY date_time ASC
                LIMIT 1
            )
            
            LEFT JOIN matches last_m ON last_m.match_id = (
                SELECT match_id FROM matches
                WHERE (match_keeper = t.team_id)
                AND datetime(date_time) < datetime('now', 'localtime')
                ORDER BY date_time DESC
                LIMIT 1
            )
            
            WHERE t.contact_person = ?
            OR t.contact_person_2 = ?
            OR r.player_id = ?
        ''', (user_id, user_id, user_id)).fetchall()
    finally:
        conn.close()

    return render_template('my_team.html', teams = teams, facs=facilities_data, u_id = user_id)

@teams_bp.route('/my_team/create', methods=['POST', 'GET'])
def create_team():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        team_count_row = cursor.execute('''
            SELECT COUNT (*) as count
            FROM teams
            WHERE contact_person = ? OR contact_person_2 = ?
        ''', (user_id, user_id)).fetchone()

        if team_count_row['count'] >= 3:
            flash("You have reached the maximum amount of teams manageable", "danger")
            return redirect(url_for('teams.my_team'))

        name = request.form.get('name')
        file = request.files.get('logo')
        color = request.form.get('color')
        facility = request.form.get('facility')
        logo_filename = None

        if file and file.filename != '':
            logo_filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename))

        if not name or not color:
            flash("Form filled out incorrectly", "danger")
            return redirect(url_for('teams.my_team'))

        cursor.execute('''
            INSERT INTO teams (name, contact_person, logo, colour, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, user_id, logo_filename, color, facility,))

        conn.commit()
    finally:
        conn.close()
    
    flash("New team created!", "success")
    return redirect(url_for('teams.my_team'))

@teams_bp.route('/team/delete/<int:t_id>')
def delete_team(t_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        permissions_pass = cursor.execute('SELECT * from teams WHERE team_id = ? AND (contact_person = ? OR contact_person2 = ?)', (t_id, user_id)).fetchone()
        if not permissions_pass:
            flash('You do not have permissions to delete this team')
            return redirect(url_for('teams.my_team'))

        cursor.execute('DELETE FROM teams WHERE team_id = ?', (t_id,))

        conn.commit()
    finally:
        conn.close()

    flash("Team deleted!", "success")
    return redirect(url_for('teams.my_team'))

@teams_bp.route('/team/edit/<int:t_id>', methods=['POST'])
def edit_team(t_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    name = request.form.get('name')
    file = request.files.get('logo')
    color = request.form.get('color')
    facility = request.form.get('facility')
    logo_filename = None

    if file and file.filename != '':
        logo_filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename))

    if not name or not color:
        flash("Team not edited! (form filled out incorrectly)", "danger")
        return redirect(url_for('teams.my_team'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE teams 
            SET name = ?, logo = ?, colour = ?, location = ?
            WHERE team_id = ?
        ''', (name, logo_filename, color, facility, t_id,))

        conn.commit()
    finally:
        conn.close()

    flash("Team edited successfully!", "success")
    return redirect(url_for('teams.my_team'))

@teams_bp.route('/team_detail/<int:t_id>')
def team_detail(t_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        team_data = cursor.execute('SELECT * FROM teams WHERE team_id = ?', (t_id,)).fetchone()

        if not team_data:
            flash('Team not found', 'danger')
            return all_teams()

        roster_data = get_roster_data(t_id)

    finally:
        conn.close()

    return render_template('team_detail.html', team=team_data, roster=roster_data)

@teams_bp.route('/all_teams')
def all_teams():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        teams_data = cursor.execute('SELECT * FROM teams').fetchall()

    finally:
        conn.close()

    return render_template('all_teams.html', teams=teams_data)