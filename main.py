
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- Artifacts Setup ---
FLAGGED_BREAKERS_PATH = 'flagged_breakers.json'
# ----------------------

# Load users from users.json
with open('users.json', 'r') as f:
    users_data = json.load(f)
    users = {user['username']: {'password': user['password'], 'role': user['role']} for user in users_data['users']}

# Load flagged breakers
if os.path.exists(FLAGGED_BREAKERS_PATH):
    with open(FLAGGED_BREAKERS_PATH, 'r') as f:
        flagged_breakers = json.load(f)
else:
    flagged_breakers = []

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for(f"{session['role']}_console"))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin_console():
    if 'username' in session and session['role'] == 'admin':
        with open('circuit_breakers.json', 'r') as f:
            data = json.load(f)
        return render_template('admin_console.html', circuit_breakers=data['circuit_breakers'], flagged_breakers=flagged_breakers)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/dashboard/data')
def dashboard_data():
    if 'username' in session and session['role'] == 'admin':
        with open('circuit_breakers.json', 'r') as f:
            data = json.load(f)
        
        # Simulate real-time data changes
        for breaker in data['circuit_breakers']:
            breaker['current'] = round(breaker['current'] + random.uniform(-5, 5), 2)
            breaker['voltage'] = round(breaker['voltage'] + random.uniform(-1, 1), 2)
            breaker['temperature'] = round(breaker['temperature'] + random.uniform(-2, 2), 2)
            
            # Update status based on simulated values
            if breaker['temperature'] > 80 or breaker['current'] > 400:
                breaker['status'] = 'Alert'
            elif breaker['temperature'] > 60 or breaker['current'] > 300:
                breaker['status'] = 'Warning'
            else:
                breaker['status'] = 'Operational'
        
        # Save historical data
        with open('historical_data.json', 'r+') as f:
            try:
                historical_data = json.load(f)
            except json.JSONDecodeError:
                historical_data = []

            historical_entry = {
                'timestamp': datetime.now().isoformat(),
                'circuit_breakers': data['circuit_breakers']
            }
            historical_data.append(historical_entry)
            f.seek(0)
            json.dump(historical_data, f, indent=4)

        return jsonify(data)
    return redirect(url_for('login'))

@app.route('/technician')
def technician_console():
    if 'username' in session and session['role'] == 'technician':
        with open('circuit_breakers.json', 'r') as f:
            all_breakers = json.load(f)['circuit_breakers']
        
        flagged_breaker_details = [breaker for breaker in all_breakers if breaker['id'] in flagged_breakers]

        return render_template('technician_console.html', flagged_breakers=flagged_breaker_details)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Use Gunicorn to run the application
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': f'0.0.0.0:{os.environ.get("PORT", 5000)}',
        'workers': 4,
    }

    StandaloneApplication(app, options).run()
