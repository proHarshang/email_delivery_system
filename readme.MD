# Email Delivery System

## Overview
This project is a simple email delivery system built with Flask, allowing users to send emails, schedule emails, and view sent emails stored in an SQLite database. Users can also send emails with attachments and schedule bulk emails.

## Features
- Send single emails with attachments.
- Send bulk emails at specified intervals.
- Schedule emails to be sent at a specific time.
- View sent emails with details like sender, recipients, subject, and time sent.
- Delete emails from the log.

## Technologies Used
- Python
- Flask
- SQLite
- jQuery
- HTML/CSS

## Setup Instructions

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd email_delivery_system

2. Install required packages:
    ```bash
    pip install Flask
    pip install APScheduler

### Database Initialization
- The project uses SQLite to store email logs. The database will be created automatically when you run the application for the first time.

### Running the Application
1. Start the Flask server:
    python app.py

2. Open your browser and navigate to http://127.0.0.1:5000.

### API Endpoints
1. POST /send_mail: Send a single email.
2. POST /send_bulk_email: Schedule bulk emails.
3. POST /schedule_email: Schedule an email for a specific time.
4. GET /view_emails: View sent emails.
5. POST /delete_email/<id>: Delete an email log entry

### Usage
1. Use the form on the home page to send or schedule emails.
2. Navigate to the "View Emails" page to see the emails you've sent and delete them if needed.

### Note
1. Make sure to configure your email server settings (e.g., Gmail SMTP) within the send_email function in app.py.
2. For production use, consider securing sensitive data like email credentials.

### Acknowledgments
1. Flask
2. APScheduler
3. SQLite