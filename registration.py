from flask import Blueprint, render_template, request, send_file
import sqlite3, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

bp = Blueprint('registration', __name__)

@bp.route('/registration')
def registration():
    return render_template('reg.html')

@bp.route('/submit_registration', methods=['POST'])
def submit_registration():
    data = {
        'current_date': request.form.get('current_date'),
        'student_name': request.form.get('student_name'),
        'student_class': request.form.get('class'),
        'father_name': request.form.get('father_name'),
        'mother_name': request.form.get('mother_name'),
        'address': request.form.get('address'),
        'contact_number': request.form.get('contact_number'),
        'test_date': request.form.get('test_date'),
        'last_school': request.form.get('last_school'),
        'amount': request.form.get('amount'),
        'remark': request.form.get('remark')
    }

    conn = sqlite3.connect('reg.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO registrations (
        current_date, student_name, student_class, father_name, mother_name,
        address, contact_number, test_date, last_school, amount, remark
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(data.values()))
    conn.commit()
    receipt_id = cursor.lastrowid
    conn.close()

    generate_receipt_pdf(data, receipt_id)
    receipt_url = f"/receipt/{receipt_id}"
    return render_template('success.html', receipt_url=receipt_url)

@bp.route('/receipt/<int:receipt_id>')
def serve_receipt(receipt_id):
    file_path = f"receipts/receipt_{receipt_id}.pdf"
    return send_file(file_path, mimetype='application/pdf')

def generate_receipt_pdf(data, receipt_id):
    folder = "receipts"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"receipt_{receipt_id}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, "SHARDA INTERNATIONAL SCHOOL")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 60, "Registration Receipt")

    y = height - 100
    line_gap = 18
    fields = [
        ("Receipt No", receipt_id),
        ("Date", data['current_date']),
        ("Student Name", data['student_name']),
        ("Class", data['student_class']),
        ("Father's Name", data['father_name']),
        ("Mother's Name", data['mother_name']),
        ("Address", data['address']),
        ("Contact No", data['contact_number']),
        ("Test Date", data['test_date']),
        ("Last School", data['last_school']),
        ("Amount Paid", f"₹{data['amount']}"),
        ("Remark", data['remark']),
    ]

    c.setFont("Helvetica", 11)
    for label, value in fields:
        c.drawString(40, y, f"{label}:")
        c.drawString(150, y, str(value))
        y -= line_gap

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 60, "This is a system-generated receipt. No signature required.")
    c.drawRightString(width - 40, 60, "Thank you!")
    c.save()
