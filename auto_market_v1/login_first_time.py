from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

CHROME_DRIVER_PATH = "C:\\chromedriver\\chromedriver.exe"

# Setăm Chrome fără profil (browser curat)
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--start-maximized")

if not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"ChromeDriver not found at: {CHROME_DRIVER_PATH}")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Anti-Selenium detection trick
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Deschidem pagina de login Facebook
driver.get("https://www.facebook.com/")

print("\n🔑 Browserul este deschis. Te rog să te loghezi manual pe Facebook.")

# Lasă browserul deschis cât vrei
input("\n📌 Apasă Enter când ai terminat logarea și vrei să închizi browserul...")

driver.quit()
print("\n✅ Browser închis.")
