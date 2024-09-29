import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            role TEXT,
            issue TEXT,
            priority TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

# Route to handle ticket form submission
@app.route('/submit-ticket', methods=['POST'])
def submit_ticket():
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']
    issue = request.form['issue']
    priority = request.form['priority']

    # Save the data to the SQLite database
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (name, email, role, issue, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, role, issue, priority))
    conn.commit()
    conn.close()

    # Flash success message
    flash(f"Ticket submitted successfully by {name} ({role}) with priority: {priority}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
