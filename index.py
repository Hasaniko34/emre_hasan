from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'finvision_secret_key'

# Basit kullanıcı yönetimi
users = {
    'demo@example.com': {
        'password': 'demo123',
        'first_name': 'Demo',
        'last_name': 'Kullanıcı'
    }
}

# Proje kök dizini
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    """Ana sayfa - Landing page"""
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası"""
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
    """Dashboard / Analiz sayfası"""
    # Genişletilmiş şirket listesi
    us_companies = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'JPM', 'JNJ', 'XOM'
    ]
    
    tr_companies = [
        'AKBNK.IS', 'THYAO.IS', 'EREGL.IS', 'GARAN.IS', 'TUPRS.IS', 'BIMAS.IS', 'KCHOL.IS', 
        'YKBNK.IS', 'ASELS.IS', 'SISE.IS'
    ]
    
    return render_template('index.html', 
                          last_analysis_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          has_results=True,
                          us_companies=us_companies,
                          tr_companies=tr_companies)

@app.route('/results')
def results():
    """Sonuçlar sayfası"""
    return render_template('results.html')

@app.route('/report')
def report():
    """Rapor sayfası"""
    return render_template('report.html')

@app.route('/api/chart-data')
def chart_data():
    """API - Grafik verileri için"""
    try:
        # Örnek veri oluştur
        data = {
            "carComparison": {
                "labels": ["Temettü", "Hisse Geri Alımı"],
                "datasets": [
                    {
                        "label": "Ortalama CAR (%)",
                        "data": [2.3, 3.7]
                    }
                ]
            },
            "carDistribution": {
                "labels": ["< -5%", "-5% - 0%", "0% - 5%", "5% - 10%", "> 10%"],
                "datasets": [
                    {
                        "label": "Temettü",
                        "data": [10, 15, 40, 25, 10]
                    },
                    {
                        "label": "Hisse Geri Alımı",
                        "data": [5, 10, 35, 35, 15]
                    }
                ]
            },
            "financialMetrics": {
                "labels": ["ROE (%)", "ROA (%)", "Kâr Marjı (%)", "Borç/Özkaynak"],
                "datasets": [
                    {
                        "label": "Temettü Veren Şirketler",
                        "data": [15.2, 8.1, 12.3, 0.45]
                    },
                    {
                        "label": "Hisse Geri Alımı Yapan Şirketler",
                        "data": [16.8, 9.2, 13.7, 0.38]
                    }
                ]
            },
            "sectorAnalysis": {
                "labels": ["Finans", "Teknoloji", "Sanayi", "Tüketici", "Enerji"],
                "datasets": [
                    {
                        "label": "Temettü CAR (%)",
                        "data": [1.8, 2.5, 2.1, 2.7, 1.9]
                    },
                    {
                        "label": "Hisse Geri Alımı CAR (%)",
                        "data": [2.9, 4.1, 3.5, 3.8, 3.2]
                    }
                ]
            },
            "timeSeries": {
                "labels": ["2018", "2019", "2020", "2021", "2022", "2023"],
                "datasets": [
                    {
                        "label": "Temettü CAR (%)",
                        "data": [2.1, 1.9, 2.3, 2.6, 2.4, 2.5]
                    },
                    {
                        "label": "Hisse Geri Alımı CAR (%)",
                        "data": [3.2, 3.5, 3.9, 4.2, 3.8, 3.6]
                    }
                ]
            }
        }
        
        return jsonify(data)
    except Exception as e:
        print(f"Grafik verileri alınırken hata: {str(e)}")
        # Hata durumunda boş veri döndür
        return jsonify({})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 