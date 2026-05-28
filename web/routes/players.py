from flask import Blueprint, render_template
from database import get_db_connection

players_bp = Blueprint('players', __name__)

@players_bp.route('/all_players')
def all_players():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        players_data = cursor.execute('''
            SELECT

            m.full_name as name,
            m.member_id as member_id,
            p.jersey_number as jersey_number

            FROM members m JOIN players p 
            ON m.member_id = p.member_id
        ''').fetchall()
    finally:
        conn.close()

    return render_template('all_players.html', players=players_data)