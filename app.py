from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import sqlite3

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# SQLite DB functions 
def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receivers TEXT,
            subject TEXT,
            time_sent DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Call this at the start of your app

def log_email(sender, receivers, subject):
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO email_logs (sender, receivers, subject, time_sent)
        VALUES (?, ?, ?, datetime('now'))
    ''', (sender, ', '.join(receivers), subject))
    conn.commit()
    conn.close()


# Email sending function
def send_email(sender, password, receivers, subject, body, attachments=[]):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.set_content(body)

    # Loop through attachments and add them to the email
    for attachment in attachments:
        # Ensure the attachment file exists before trying to attach
        if os.path.exists(attachment):
            with open(attachment, 'rb') as f:
                file_data = f.read()
                  # Extract the file name from the file path
                file_name = os.path.basename(attachment)
                 # Add the attachment to the email
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        else:
            print(f"Warning: Attachment {attachment} does not exist.")

    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
        
    # Log email    
    log_email(sender, receivers, subject)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
    try: 
        # Debugging prints to check request
        print("Request form:", request.form)
        print("Request files:", request.files)
        
        form_data = request.form
        sender = form_data['sender']
        password = form_data['password'] 
        receivers = json.loads(form_data['receivers'])  # Convert stringified receivers array back to list
        subject = form_data['subject']
        body = form_data['body']      
        
        attachments = []
        if 'attachments' in request.files:
            uploaded_files = request.files.getlist('attachments')
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    attachments.append(file_path)            
                else:
                    print(f"Warning: {file.filename} is not allowed.")
        else:
            attachments = []  
        
        send_email(sender, password, receivers, subject, body, attachments)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print("Error occurred:", str(e))  # Print the error for debugging
        return jsonify({"message": str(e)}), 400

@app.route('/send_bulk_email', methods=['POST'])
def send_bulk_email():
    try:
        # Debugging prints to check request
        print("Request form:", request.form)
        print("Request files:", request.files)
        
        form_data = request.form
        sender = form_data['sender']
        password = form_data['password']
        receivers = json.loads(form_data['receivers'])  # Convert stringified receivers array back to list
        subject = form_data['subject']
        body = form_data['body']
        num_emails = int(form_data['numEmails'])
        interval = int(form_data['interval'])
        
         # Handle attachments
        attachments = []
        if 'attachments' in request.files:
            uploaded_files = request.files.getlist('attachments')
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    attachments.append(file_path)
                else:
                    print(f"Warning: {file.filename} is not allowed.")
        else:
            attachments = []
        
        # Schedule email sending here
        for i in range(num_emails):
            scheduler.add_job(
                send_email,
                'date',
                run_date=datetime.now() + timedelta(minutes=i * interval),
                args=[sender, password, receivers, subject, body, attachments]
            )
        return jsonify({"message": "Bulk email scheduled!"}), 200
    except Exception as e:
        print("Error occurred:", str(e))  # Print the error for debugging
        return jsonify({"message": str(e)}), 400

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    try:
        # Debugging prints to check request
        print("Request form:", request.form)
        print("Request files:", request.files)
        
        # Extract form data
        form_data = request.form
        sender = form_data['sender']
        password = form_data['password']
        receivers = json.loads(form_data['receivers'])  # Convert stringified receivers array back to list
        subject = form_data['subject']
        body = form_data['body']
        schedule_time = datetime.fromisoformat(form_data['scheduleTime'])
        
         # Handle attachments
        attachments = []
        if 'attachments' in request.files:
            uploaded_files = request.files.getlist('attachments')
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    attachments.append(file_path)
                else:
                     print(f"Warning: {file.filename} is not allowed.")
        else:
            attachments = []
        
        scheduler.add_job(
            send_email,
            'date',
            run_date=schedule_time,
            args=[sender, password, receivers, subject, body, attachments]
        )
        return jsonify({"message": "Email scheduled!"}), 200
    except Exception as e:
        print("Error occurred:", str(e))  # Print the error for debugging
        return jsonify({"message": str(e)}), 400

@app.route('/view_emails')
def view_emails():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('SELECT id, sender, receivers, subject, time_sent FROM email_logs')
    emails = c.fetchall()
    conn.close()
    return render_template('view_emails.html', emails=emails)

@app.route('/delete_email/<int:id>', methods=['POST'])
def delete_email(id):
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('DELETE FROM email_logs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Email deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
