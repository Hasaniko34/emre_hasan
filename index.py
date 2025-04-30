from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/report')
def report():
    return render_template('report.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 