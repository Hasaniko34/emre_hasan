from flask import Flask, render_template, redirect, url_for, request, session, jsonify

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
    
    last_analysis_time = "2023-11-01 14:30:00"
    
    return render_template('index.html', 
                          last_analysis_time=last_analysis_time,
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
        # Hata durumunda boş veri döndür
        return jsonify({})

@app.route('/api/results', methods=['GET'])
def get_results_json():
    """API - Sonuçlar için JSON verisi"""
    try:
        # Örnek sonuçlar
        results = {
            "event_study": [
                {"company": "AAPL", "event_type": "Buyback", "event_date": "2022-05-15", "car": 3.8, "t_stat": 2.4, "p_value": 0.02},
                {"company": "MSFT", "event_type": "Buyback", "event_date": "2022-06-10", "car": 4.2, "t_stat": 2.6, "p_value": 0.01},
                {"company": "GOOGL", "event_type": "Dividend", "event_date": "2022-04-22", "car": 2.5, "t_stat": 1.9, "p_value": 0.06},
                {"company": "AMZN", "event_type": "Buyback", "event_date": "2022-07-05", "car": 3.5, "t_stat": 2.2, "p_value": 0.03},
                {"company": "META", "event_type": "Dividend", "event_date": "2022-03-18", "car": 1.9, "t_stat": 1.7, "p_value": 0.09}
            ],
            "financial_analysis": [
                {"company": "AAPL", "event_type": "Buyback", "roe": 157.8, "roa": 28.5, "profit_margin": 25.9, "debt_to_equity": 1.56},
                {"company": "MSFT", "event_type": "Buyback", "roe": 47.1, "roa": 19.3, "profit_margin": 36.7, "debt_to_equity": 0.46},
                {"company": "GOOGL", "event_type": "Dividend", "roe": 30.3, "roa": 16.9, "profit_margin": 27.1, "debt_to_equity": 0.28},
                {"company": "AMZN", "event_type": "Buyback", "roe": 28.9, "roa": 7.1, "profit_margin": 5.5, "debt_to_equity": 1.22},
                {"company": "META", "event_type": "Dividend", "roe": 24.7, "roa": 16.9, "profit_margin": 31.2, "debt_to_equity": 0.37}
            ]
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({})

@app.route('/api/report-content')
def get_report_content():
    """API - Rapor içeriği için"""
    try:
        report_content = """# Hisse Geri Alımı ve Temettü Etki Analizi Raporu

## 1. Özet
Bu rapor, hisse geri alımı ve temettü duyurularının hisse senedi fiyatları üzerindeki etkisini analiz etmektedir.

## 2. Olay Çalışması Sonuçları
| Company | Event Type | Event Date | CAR | t-stat | p-value |
|---------|------------|------------|-----|--------|---------|
| AAPL    | Buyback    | 2022-05-15 | 3.8 | 2.4    | 0.02    |
| MSFT    | Buyback    | 2022-06-10 | 4.2 | 2.6    | 0.01    |
| GOOGL   | Dividend   | 2022-04-22 | 2.5 | 1.9    | 0.06    |
| AMZN    | Buyback    | 2022-07-05 | 3.5 | 2.2    | 0.03    |
| META    | Dividend   | 2022-03-18 | 1.9 | 1.7    | 0.09    |

## 3. Finansal Analiz
| Company | Event Type | ROE (%) | ROA (%) | Profit Margin (%) | Debt/Equity |
|---------|------------|---------|---------|-------------------|-------------|
| AAPL    | Buyback    | 157.8   | 28.5    | 25.9              | 1.56        |
| MSFT    | Buyback    | 47.1    | 19.3    | 36.7              | 0.46        |
| GOOGL   | Dividend   | 30.3    | 16.9    | 27.1              | 0.28        |
| AMZN    | Buyback    | 28.9    | 7.1     | 5.5               | 1.22        |
| META    | Dividend   | 24.7    | 16.9    | 31.2              | 0.37        |

## 4. Karşılaştırmalı Analiz
Hisse geri alımı yapan şirketler ortalama olarak daha yüksek CAR değerlerine sahiptir. Ortalama CAR değeri temettü için %2.3, hisse geri alımı için %3.7 olarak hesaplanmıştır.

## 5. Sonuç ve Öneriler
Analiz sonuçlarına göre:
1. Hisse geri alım duyuruları ortalama olarak daha yüksek anormal getiri sağlamaktadır.
2. Temettü duyuruları da pozitif ancak daha düşük bir etkiye sahiptir.
3. Finansal göstergeler açısından her iki politika da benzer sonuçlar göstermektedir.

Rapor Oluşturma Tarihi: 2023-11-01 14:30
"""
        
        return jsonify({"content": report_content})
    except Exception as e:
        return jsonify({"content": "Rapor yüklenirken bir hata oluştu."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 