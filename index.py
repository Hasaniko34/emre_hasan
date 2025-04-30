import os
import sys

# Uygulama dizinini ekleyin
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from flask import Flask, render_template, redirect, url_for, request, flash, session
from app import app

app.secret_key = 'finvision_secret_key'  # Gerçek uygulamada güvenli bir değer kullanın

# Basit kullanıcı yönetimi
users = {
    'demo@example.com': {
        'password': 'demo123',
        'first_name': 'Demo',
        'last_name': 'Kullanıcı'
    }
}

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['first_name'] = users[email]['first_name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Geçersiz e-posta veya şifre.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/report')
def report():
    return render_template('report.html')

# Vercel için uygulama başlatıcı
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 