from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)
app.secret_key = 'finvision_secret_key'

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
        
        if email == 'demo@example.com' and password == 'demo123':
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Geçersiz e-posta veya şifre.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard / Analiz sayfası"""
    return render_template('index.html')

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
        # Minimal örnek veri
        data = {
            "carComparison": {
                "labels": ["Temettü", "Hisse Geri Alımı"],
                "datasets": [
                    {
                        "label": "Ortalama CAR (%)",
                        "data": [2.3, 3.7]
                    }
                ]
            }
        }
        return jsonify(data)
    except Exception:
        return jsonify({})

@app.route('/test')
def test():
    """Test endpoint'i"""
    return "Flask uygulaması çalışıyor!"

if __name__ == "__main__":
    app.run() 