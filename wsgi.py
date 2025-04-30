from app import app

# Render için WSGI uygulaması
if __name__ == "__main__":
    app.run(host='0.0.0.0') 