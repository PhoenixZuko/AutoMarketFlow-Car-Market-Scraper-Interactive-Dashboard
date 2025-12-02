import os
import time
import hashlib
import random
import csv
import tempfile
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

def create_driver(headless=False, user_data_dir=None):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
    else:
        # Folosește un profil temporar random pentru a preveni salvarea sesiunii
        temp_profile = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_profile}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--disable-infobars")
    options.add_argument("--incognito")  # nici sesiune, nici cache

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"},
    )
    return driver

def get_city_code(city_name):
    return city_name.split(",")[0].replace(" ", "").lower()

def build_url(city_code, config):
    base_url = f"https://{city_code}.craigslist.org/search/cta"
    params = f"?search_distance={config['search_distance']}&postal=&purveyor={config['purveyor']}"
    params += f"&min_auto_year={config['min_year']}&max_auto_year={config['max_year']}"
    params += f"&min_auto_miles={config['min_miles']}&max_auto_miles={config['max_miles']}"
    return base_url + params

def clean_filename(link):
    return hashlib.md5(link.encode()).hexdigest()

def try_get(driver, url, retries=3):
    for attempt in range(retries):
        try:
            driver.get(url)
            time.sleep(random.uniform(1.5, 2.5))  # Așteptare inițială

            # 👇 Simulează scroll random
            scrolls = random.randint(1, 3)
            for _ in range(scrolls):
                y = random.randint(200, 1000)
                driver.execute_script(f"window.scrollBy(0, {y});")
                time.sleep(random.uniform(0.5, 1.2))

            # 👇 Mișcare mouse într-o zonă aleatorie (doar script)
            x = random.randint(100, 400)
            y = random.randint(100, 400)
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                document.body.dispatchEvent(event);
            """)

            # 👇 Click fals pe body (nu afectează pagina)
            driver.execute_script("document.body.click();")

            return True

        except (WebDriverException, TimeoutException) as e:
            print(f"⚠️  Attempt {attempt+1} failed: {e}")
            time.sleep(random.uniform(3, 6))
    print(f"❌ Failed to load {url} after {retries} retries.")
    return False


def save_csv(log_file, rows):
    write_header = not os.path.exists(log_file) or os.stat(log_file).st_size == 0
    with open(log_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["URL", "Title", "City", "MinYear", "MaxYear", "KM-Range"])
        for row in rows:
            writer.writerow(row)

def log_error(message):
    with open("logs/error_log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def run_scraper(config):
    log_file = "logs/log.csv"
    save_folder = "craig_saved_pages"
    temp_profile = tempfile.mkdtemp()  # profil temporar, fără sesiuni salvate

    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    seen_links = set()
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            seen_links = set(line.split(",")[0].strip() for line in f if line.strip())

    driver = create_driver(config.get("headless", False), temp_profile)

    for city in config.get("city_list", []):
        try:
            city_name = city.strip()
            city_code = get_city_code(city_name)
            city_display = city_name.replace(",", " -")

            print(f"\n🌆 City: {city_display}")
            url = build_url(city_code, config)
            print(f"🔗 URL: {url}")

            if not try_get(driver, url):
                continue

            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ad_links = set()

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/cto/d/" in href:
                    if not href.startswith("http"):
                        href = f"https://{city_code}.craigslist.org{href}"
                    if href not in seen_links:
                        ad_links.add(href)

            print(f"📦 Found {len(ad_links)} new ads")
            time.sleep(random.uniform(1, 2))

            for link in ad_links:
                try:
                    print(f"📥 Opening: {link}")
                    if not try_get(driver, link):
                        continue

                    time.sleep(random.uniform(2, 4))
                    html = driver.page_source
                    soup_detail = BeautifulSoup(html, "html.parser")
                    text = soup_detail.get_text(separator="\n", strip=True)
                    title = soup_detail.title.text.strip() if soup_detail.title else "No Title"

                    file_basename = clean_filename(link)
                    file_path = os.path.join(save_folder, file_basename + ".txt")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"URL: {link}\nTITLE: {title}\n\n{text}")

                    row = [
                        link,
                        title,
                        city_display,
                        config['min_year'],
                        config['max_year'],
                        f"{config['min_miles']}-{config['max_miles']}"
                    ]
                    save_csv(log_file, [row])
                    seen_links.add(link)
                except Exception as e:
                    error_msg = f"❌ Error processing ad: {link} | {e}"
                    print(error_msg)
                    log_error(error_msg)
                    continue

            print(f"✅ Finished with {city_display}, sleeping before next...\n")
            time.sleep(random.uniform(4, 7))

        except Exception as e:
            error_msg = f"❌ Error processing city: {city} | {e}"
            print(error_msg)
            log_error(error_msg)
            continue

    driver.quit()
    print("\n✅ Done! All ads have been saved.")
