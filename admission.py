from flask import Blueprint, render_template, request
import sqlite3

bp = Blueprint('admission', __name__)

@bp.route('/admission')
def admission():
    return render_template('form.html')

@bp.route('/submit_admission', methods=['POST'])
def submit_admission():
    fname = request.form['fname']
    lname = request.form['lname']
    faname = request.form['faname']
    email = request.form['email']
    dob = request.form['dob']
    gender = request.form['gender']
    course = request.form['course']
    address = request.form['address']

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT,
        lname TEXT,
        faname TEXT,
        email TEXT,
        dob TEXT,
        gender TEXT,
        course TEXT,
        address TEXT
    )''')
    cursor.execute('''INSERT INTO admissions 
        (fname, lname, faname, email, dob, gender, course, address) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (fname, lname, faname, email, dob, gender, course, address))
    conn.commit()
    conn.close()
    return render_template('success.html', name=fname)
