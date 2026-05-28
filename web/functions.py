from database import get_db_connection
from flask import session, redirect, url_for

def get_roster_data(t_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    data_list = []

    data_list.append(cursor.execute('''SELECT r.*, m.*, p.* FROM rosters r
                                        JOIN members m ON r.player_id = m.member_id
                                        JOIN players p ON m.member_id = p.member_id
                                        WHERE r.team_id = ?''',(t_id,)).fetchall())
    
    conn.close()
    return data_list
