from flask import Flask
from routes import setup_routes
import webbrowser
import threading

app = Flask(__name__, template_folder='templates', static_folder='static')

# Setăm rutele modular
setup_routes(app)

def open_browser():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open_new('http://127.0.0.1:5005/')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)
