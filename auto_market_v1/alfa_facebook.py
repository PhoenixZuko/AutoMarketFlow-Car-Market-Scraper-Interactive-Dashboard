import os
import signal
import subprocess
import time
import yaml
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Salvăm PID în același folder cu acest fișier (unde este și start_faceboock.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PID_FILE = os.path.join(BASE_DIR, "program_pid.txt")

with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

from facebook.clean_session import fix_chrome_profile
from facebook.facebook_task_extractor import run_marketplace_extraction
from facebook.search_loader import load_facebook_search_tasks
from facebook.auto_scroll import auto_scroll_until_no_new

# 📁 Path-uri
CHROME_DRIVER_PATH = "C:\\chromedriver\\chromedriver.exe"
CONFIG_PATH = "config/config.yaml"
FACEBOOK_SEARCH_CONFIG = "config/facebook.yaml"

# 🛠️ Funcție clean_exit pentru semnale
def clean_exit(signum, frame):
    print(f"\n🛑 Received signal {signum}. Closing Chrome and exiting gracefully...")
    try:
        driver.quit()
    except Exception as e:
        print(f"⚠️ Error closing driver: {e}")
    exit(0)

# 🔔 Funcție pentru click pe notificări și messenger dacă există badge roșu
def clear_all_notifications(driver):
    try:
        print("[🔔] Waiting for the notifications icon...")
        notif_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Notifications' or @aria-label='Notificări']"))
        )
        driver.execute_script("arguments[0].click();", notif_icon)
        time.sleep(3)

        print("[📜] Checking if the popup appeared...")
        dialog = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
        time.sleep(2)

        print("[🔍] Searching for links to notifications..")
        links = dialog.find_elements(By.XPATH, ".//a[contains(@href, '/notifications/')]")

        if not links:
            print("[ℹ️] No notifications available.")
            return

        print(f"[✅] Found  {len(links)} notifications. Opening the first one...")
        driver.execute_script("arguments[0].click();", links[0])
        time.sleep(5)

        print("[↩️] Returning to facebook.com...")
        driver.get("https://www.facebook.com/")
        time.sleep(5)

        # Verificăm din nou iconița
        notif_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Notifications' or @aria-label='Notificări']"))
        )
        badge = notif_icon.find_elements(By.XPATH, ".//span[contains(@style,'background-color')]")

        if not badge:
            print("[✅] The notification badge has been removed")
        else:
            print("[❌] The badge is still visible.")
    except Exception as e:
        print(f"[❌]Error while processing notifications: {e}")



def clear_all_messenger(driver):
    try:
        messenger_icons = driver.find_elements(By.CSS_SELECTOR, "div[aria-label*='Messenger']")
        if not messenger_icons:
            return  # No Messenger icon found

        icon = messenger_icons[0]
        badge = icon.find_elements(By.XPATH, ".//span[contains(@style,'background-color')]")
        if not badge:
            return  # No badge → silently skip

        driver.execute_script("arguments[0].click();", icon)
        time.sleep(2)

        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'x78zum5') and contains(@class,'x1q0g3np')]"))
        )
        for _ in range(3):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            time.sleep(1)

        print("[🧼] Messenger badge cleared.")
    except Exception as e:
        print(f"[❌] Error clearing Messenger: {e}")



def scroll_notification_popup(driver):
    print("[📜] Attempting to scroll through notifications to mark them as read...")
    try:
        # Așteaptă div-ul de notificări
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'x78zum5') and contains(@class,'x1q0g3np')]"))
        )

        # Derulează în jos de câteva ori
        for _ in range(5):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            time.sleep(1)
        print("[✅] Scroll completed.")
    except Exception as e:
        print(f"[❌] Error while scrolling through notifications: {e}")


# 🛠️ Încarcă config.yaml
print("[1] Loading configuration from config.yaml...")
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

profile_name = config.get("active_profile")
profile_data = config["profiles"].get(profile_name)

if not profile_data:
    raise ValueError(f"Active profile '{profile_name}' does not exist in config.yaml")

user_data_dir = profile_data["user_data_dir"]
resolution = profile_data["resolution"]

# 🛡️ Fixăm profilul Chrome înainte să pornim browser-ul
fix_chrome_profile(user_data_dir)

# 🛡️ Setăm handlers pentru semnale
signal.signal(signal.SIGINT, clean_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, clean_exit)  # kill
signal.signal(signal.SIGBREAK, clean_exit) # Ctrl+Break (CTRL_BREAK_EVENT)

# 🛠️ Configurare Chrome
print(f"[2] Launching Chrome with profile: {profile_name}")

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--start-maximized")

width, height = resolution.split(",")
chrome_options.add_argument(f"--window-size={width},{height}")

# ➕ Opțiuni extra pentru stabilitate
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 🛠️ Verificare ChromeDriver
if not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"ChromeDriver not found at: {CHROME_DRIVER_PATH}")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 🧠 Anti-Selenium trick
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 🔗 Navigăm către pagina principală Facebook (obligatoriu pentru clopoțel!)
print("[🌐] We navigate to facebook.com...")
driver.get("https://www.facebook.com/")
time.sleep(5)  # Așteptăm încărcarea completă a interfeței

# 🔔 Curățăm notificările și Messenger-ul
try:
    print("[🔔] We are waiting for the notification icon to appear...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Notifications' or @aria-label='Notificări']"))
    )
    clear_all_notifications(driver)
    clear_all_messenger(driver)
except Exception as e:
    print(f"[⚠️] Could not clear notifications or Messenger: {e}")


# ✅ Citim taskurile din facebook.yaml
print("[3] Loading Facebook search tasks...")
search_tasks = load_facebook_search_tasks(FACEBOOK_SEARCH_CONFIG)

# ✅ Rulăm pentru fiecare oraș
first_city = True

for task in search_tasks:
    city = task.get('city')
    price_min = task.get('price_min')
    price_max = task.get('price_max')

    print(f"\n🔍 Running task for city: {city} | price min: {price_min} | price max: {price_max}")

    start_time = time.time()

    # ✅ Deschide Marketplace
    run_marketplace_extraction(driver, task)

    # ✅ Executăm notificările și Messenger DOAR dacă e prima rundă reală
    if first_city:
        print("[📍] Marketplace loaded. Trying to fully clear notifications & messenger...")
        clear_all_notifications(driver)
        clear_all_messenger(driver)
        first_city = False

    # ➕ Scroll listings
    print(f"\n[4] Scrolling to load more listings for {city}...")
    auto_scroll_until_no_new(driver, pause_time=3, max_no_change=3)

    # ➕ Re-extragere după scroll
    print(f"[5] Collecting all loaded listings for {city}...")
    run_marketplace_extraction(driver, task)

    end_time = time.time()
    minutes, seconds = divmod(int(end_time - start_time), 60)
    print(f"\n✅ Finished with city: {city} in {minutes} minutes and {seconds} seconds.")


print("\n🎯 All cities processed. Closing browser.")
driver.quit()
print("\n[7] Starting JSON extraction from saved HTML files...")

# ✅ Varianta robustă pentru Windows
subprocess.run(["py", "extract_json_from_html.py"], check=True)

print("\n✅ JSON extraction completed.")
