from flask import Flask, render_template, redirect, url_for , request
import subprocess
import os
import sys
import psutil  # pentru PID-uri
import json
app = Flask(__name__, template_folder='templates')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'auto_market_v1', 'dashboard_facebook'))
DISPLAY_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'display', 'display.py'))

START_SCRIPT = os.path.join(BASE_DIR, 'start_faceboock.py')
STOP_SCRIPT = os.path.join(BASE_DIR, 'stop_facebook.py')
EXTRACTOR_SCRIPT = os.path.join(BASE_DIR, 'start_extract_json.py')
PID_FILE = os.path.join(BASE_DIR, 'program_pid.txt')




# === CRAIGSLIST SETUP ===
CRAIGLIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'auto_market_v1', 'dashboard_craiglist'))
CRAIGLIST_START_SCRIPT = os.path.join(CRAIGLIST_DIR, 'start_craiglist.py')
CRAIGLIST_STOP_SCRIPT = os.path.join(CRAIGLIST_DIR, 'stop_craiglist.py')
CRAIGLIST_EXTRACTOR_SCRIPT = os.path.join(CRAIGLIST_DIR, 'start_extract_json_craiglist.py')
CRAIGLIST_PID_FILE = os.path.join(CRAIGLIST_DIR, 'craiglist_pid.txt')

def get_craiglist_status():
    """Verifică dacă Craiglist rulează."""
    if os.path.exists(CRAIGLIST_PID_FILE):
        with open(CRAIGLIST_PID_FILE, 'r') as f:
            try:
                pid = int(f.read().strip())
                if psutil.pid_exists(pid):
                    return "Running"
            except:
                pass
    return "Stopped"

def get_craiglist_extractor_status():
    """Verifică dacă extractorul Craiglist rulează."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and 'start_extract_json_craiglist.py' in ' '.join(cmdline):
            return "Running"
    return "Stopped"


def get_status():
    """Verifică dacă Facebook Scraper rulează."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            try:
                pid = int(f.read().strip())
                if psutil.pid_exists(pid):
                    return "Running"
            except Exception as e:
                print(f"Error reading PID file: {e}")
    return "Stopped"

def get_extractor_status():
    """Verifică dacă Extractor rulează."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and isinstance(cmdline, list):
            if 'start_extract_json.py' in ' '.join(cmdline):
                return "Running"
    return "Stopped"

def get_display_status():
    """Verifică dacă Display rulează."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and isinstance(cmdline, list):
            if 'display.py' in ' '.join(cmdline):
                return "Running"
    return "Stopped"

@app.route('/')
def index():
    status = get_status()
    extractor_status = get_extractor_status()
    display_status = get_display_status() 
    return render_template('index.html', status=status, extractor_status=extractor_status, display_status=display_status)

@app.route('/start', methods=['POST'])
def start_scraper():
    print("🟢 Starting Facebook Scraper...")
    subprocess.Popen(
        [sys.executable, START_SCRIPT],
        cwd=BASE_DIR
    )
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_scraper():
    try:
        print("🔴 Stop Facebook Scraper...")
        subprocess.run(
            [sys.executable, STOP_SCRIPT],
            cwd=BASE_DIR,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error stopping process: {e}")
    return redirect(url_for('index'))


@app.route('/start_extractor', methods=['POST'])
def start_extractor():
    try:
        subprocess.Popen(
            [sys.executable, EXTRACTOR_SCRIPT],
            cwd=BASE_DIR
        )
        return redirect(url_for('index'))
    except Exception as e:
        return f"❌ Eroare la pornirea extractorului: {e}"

@app.route('/start_display', methods=['POST'])
def start_display():
    try:
        subprocess.Popen(
            ['start', 'cmd', '/k', sys.executable, DISPLAY_SCRIPT],
            cwd=os.path.dirname(DISPLAY_SCRIPT),
            shell=True
        )
        return redirect(url_for('index'))
    except Exception as e:
        return f"❌ Eroare la pornirea Display-ului: {e}"

@app.route('/stop_display', methods=['POST'])
def stop_display():
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            cmdline = proc.info.get('cmdline')
            if cmdline and isinstance(cmdline, list):
                if 'display.py' in ' '.join(cmdline):
                    proc.kill()
                    print(f"✅ Display oprit cu PID {proc.pid}")
                    break
        return redirect(url_for('index'))
    except Exception as e:
        return f"❌ Eroare la oprirea Display-ului: {e}"

@app.route('/start_craiglist', methods=['POST'])
def start_craiglist():
    subprocess.Popen([sys.executable, CRAIGLIST_START_SCRIPT], cwd=CRAIGLIST_DIR)
    return redirect(url_for('index'))

@app.route('/stop_craiglist', methods=['POST'])
def stop_craiglist():
    try:
        subprocess.run([sys.executable, CRAIGLIST_STOP_SCRIPT], cwd=CRAIGLIST_DIR, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error stopping Craiglist: {e}")
    return redirect(url_for('index'))

@app.route('/start_extractor_craiglist', methods=['POST'])
def start_extractor_craiglist():
    try:
        subprocess.Popen([sys.executable, CRAIGLIST_EXTRACTOR_SCRIPT], cwd=CRAIGLIST_DIR)
    except Exception as e:
        return f"❌ Eroare la pornirea extractorului Craiglist: {e}"
    return redirect(url_for('index'))

@app.route('/generate_yaml_craiglist', methods=['POST'])
def generate_yaml_craiglist():
    subprocess.run(["python", "auto_market_v1/dashboard_craiglist/start_generate_yaml_craig.py"], check=True)
    return redirect("/")        

    
@app.route('/generate_yaml_facebook', methods=['POST'])
def generate_yaml_facebook():
    subprocess.run(["python", "auto_market_v1/dashboard_facebook/start_generator_yaml_fb.py"], check=True)
    return redirect("/")

@app.route("/save_facebook_config", methods=["POST"])
def save_facebook_config():
    data = {
        "state": request.form.get("state"),
        "price_min": int(request.form.get("price_min", 0)),
        "price_max": int(request.form.get("price_max", 0))
    }

    # Calea completă către fișierul JSON de configurare
    config_path = os.path.join("auto_market_v1", "config", "yaml_generator", "data", "fb_form_data.json")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return redirect("/")
@app.route("/save_craig_config", methods=["POST"])
def save_craig_config():
    import os
    import json
    from flask import request, redirect

    data = {
        "state": request.form.get("state"),
        "min_year": int(request.form.get("min_year", 0)),
        "max_year": int(request.form.get("max_year", 0)),
        "min_miles": int(request.form.get("min_miles", 0)),
        "max_miles": int(request.form.get("max_miles", 0)),
        "max_ads": 99999  # valoare fixă (dacă vrei să o setezi din formular, adaugă și acel input)
    }

    config_path = os.path.join("auto_market_v1", "config", "yaml_generator", "data", "craig_form_data.json")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return redirect("/")

@app.route('/status_update')
def status_update():
    return {
        "facebook": get_status(),
        "extractor": get_extractor_status(),
        "display": get_display_status(),
        "craiglist": get_craiglist_status(),
        "craiglist_extractor": get_craiglist_extractor_status()
    }

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
