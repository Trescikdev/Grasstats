from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

facilities_bp = Blueprint('facilities', __name__)

@facilities_bp.route('/facilities', methods=['POST', 'GET'])
def facilities():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        if not user_id:
            return redirect(url_for('auth.login'))

        name = request.form.get('name')
        street = request.form.get('street')
        city = request.form.get('city')
        floortype = request.form.get('floortype')

        if not name or not street or not city or not floortype:
            flash("Facility not created! (form filled incorrectly)", "danger")
            return redirect(url_for('facilities.facilities'))

        cursor.execute('''
            INSERT INTO facilities (owner_id, name, city, street, floor_type) 
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, city, street, floortype))

        conn.commit()
        conn.close()

        flash("New facility created!", "success")
        return redirect(url_for('facilities.facilities'))

    facilities_data = cursor.execute('SELECT * from facilities').fetchall()

    conn.close()

    return render_template('facilities.html', u_id = user_id, facilities = facilities_data)

@facilities_bp.route('/facility/delete/<int:f_id>')
def delete_facility(f_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute('DELETE FROM facilities WHERE facility_id = ? AND owner_id = ?', (f_id, user_id))
        
        conn.commit()
    finally:
        conn.close()

    flash("Facility deleted!", "success")
    return redirect(url_for('facilities.facilities'))

@facilities_bp.route('/facility/edit/<int:f_id>', methods=['POST'])
def edit_facility(f_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    name = request.form.get('name')
    street = request.form.get('street')
    city = request.form.get('city')
    floortype = request.form.get('floortype')

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE facilities 
            SET name = ?, street = ?, city = ?, floor_type = ?
            WHERE facility_id = ? AND owner_id = ?
        ''', (name, street, city, floortype, f_id, user_id))

        conn.commit()
    finally:
        conn.close()

    flash("Facility updated!", "success")
    return redirect(url_for('facilities.facilities'))
