from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_db_connection
from datetime import datetime
import calendar
import functions


matches_bp = Blueprint("matches", __name__)


@matches_bp.route('/team/new_match/<int:t_id>')
def new_match(t_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        my_team_data = cursor.execute('SELECT * FROM teams WHERE team_id = ?', (t_id,)).fetchone()

        if not my_team_data:
            flash("This team doesn't exist!", "danger")
            return redirect(url_for('teams.my_team'))

        teams_data = cursor.execute('SELECT * FROM teams WHERE team_id != ?', (t_id,)).fetchall()

        roster_data = functions.get_roster_data(t_id)[0]

        facilities_data = cursor.execute('SELECT * FROM facilities').fetchall()

        home_court = None
        for i in facilities_data:
            if i[0] == my_team_data[6]:
                home_court = i[2]
    
    finally:
        conn.close()

    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = calendar.month_name[now.month]

    return render_template('new_match.html',
                           team = my_team_data,
                           teams = teams_data,
                           roster = roster_data,
                           facilities = facilities_data,
                           home = home_court,
                           cal = cal,
                           month_name = month_name,
                           year = now.year,
                           now = now,)


@matches_bp.route('/team/create_match/<int:t_id>', methods=['POST', 'GET'])
def create_match(t_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    opp = request.form.get('opponent')
    is_away = 1 if request.form.get('is_away') else 0
    lineup = request.form.getlist('selected_players')
    facility = request.form.get('facility')
    date = request.form.get('date')
    if not date or not opp:
        flash('Please fill out the form correctly!', 'danger')
        return redirect(url_for('matches.new_match'))
    if not facility or facility == "" or facility == "Choose...":
        facility = None

    home_team_id, away_team_id = t_id, opp
    if is_away:
        home_team_id, away_team_id = opp, t_id

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        #TODO POTENTIAL ISSUE DOWN BELOW (OPERATION NOT ATOMIC)
        cursor.execute('''
            INSERT INTO matches (match_keeper, home_team, away_team, date_time, facility)
            VALUES (?, ?, ?, ?, ?)
        ''', (t_id, home_team_id, away_team_id, date, facility))
        conn.commit()

        new_match_id = cursor.lastrowid

        for player in lineup:
            player = int(player)
            cursor.execute('''
                INSERT INTO match_lineups (match_id, player_id, team_side)
                VALUES (?, ?, ?)
            ''', (new_match_id, player, t_id)
            )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('teams.my_team'))


@matches_bp.route('/match_detail/<int:m_id>', methods=['GET', 'POST'])
def match_detail(m_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        match_data = cursor.execute('''
            SELECT m.*, 
                   t1.name AS home_team_name, 
                   t2.name AS away_team_name,
                   f.name AS facility_name
            FROM matches m
            LEFT JOIN teams t1 ON m.home_team = t1.team_id
            LEFT JOIN teams t2 ON m.away_team = t2.team_id
            LEFT JOIN facilities f ON m.facility = f.facility_id
            WHERE m.match_id = ?
        ''', (m_id,)).fetchone()

        if not match_data:
            flash("Match not found!", "danger")
            return redirect(url_for('teams.my_team'))

        lineup_data = cursor.execute('''
            SELECT ml.*, mem.full_name, mem.nickname
            FROM match_lineups ml
            JOIN members mem ON ml.player_id = mem.member_id
            WHERE ml.match_id = ?
        ''', (m_id,)).fetchall()

        today = datetime.now().strftime('%Y-%m-%d')
        match_date = match_data['date_time'][:10] if match_data['date_time'] else ''
    finally:
        conn.close()

    return render_template('match_detail.html', match=match_data, lineup=lineup_data, today_date=today, m_date=match_date)

@matches_bp.route('/match_in_progress/<int:m_id>')
def match_in_progress(m_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        match_data = cursor.execute('''
            SELECT m.*, 
                   t1.name AS home_team_name, 
                   t2.name AS away_team_name,
                   f.name AS facility_name
            FROM matches m
            LEFT JOIN teams t1 ON m.home_team = t1.team_id
            LEFT JOIN teams t2 ON m.away_team = t2.team_id
            LEFT JOIN facilities f ON m.facility = f.facility_id
            WHERE m.match_id = ?
        ''', (m_id,)).fetchone()

        if not match_data:
            flash("Match not found!", "danger")
            return redirect(url_for('teams.my_team'))

        lineup_data = cursor.execute('''
            SELECT ml.*, mem.full_name, mem.nickname
            FROM match_lineups ml
            JOIN members mem ON ml.player_id = mem.member_id
            WHERE ml.match_id = ?
        ''', (m_id,)).fetchall()

    finally:
        conn.close()

    return render_template('match.html', match=match_data, lineup=lineup_data)

@matches_bp.route('/team/add_match_event', methods=['POST'])
def add_match_event():
    data = request.get_json() # Načítanie JSON dát odoslaných JavaScriptom
    
    match_id = data.get('matchId')
    player_id = data.get('playerId')
    x_coord = data.get('x')
    y_coord = data.get('y')
    
    # Tu urobíš zápis do svojej databázy
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Príklad zápisu (stĺpce x_pos a y_pos si pridaj do tabuľky gólov ak ich tam nemáš)
        cursor.execute('''
            INSERT INTO goals (match_id, player_id, x_pos, y_pos)
            VALUES (?, ?, ?, ?)
        ''', (match_id, player_id, x_coord, y_coord))
        
        conn.commit()
        return jsonify({'success': True}) # Odošle odpoveď späť JavaScriptu
        
    except Exception as e:
        print(f"Chyba: {e}")
        return jsonify({'success': False}), 500
    finally:
        conn.close()