# Facebook & Craigslist Marketplace Scraper 🚀

Complete automation for extracting ads from **Facebook Marketplace** and **Craigslist**, with local saving of results and logging system to avoid duplicates.

**🔒 Note:** The browser used is separate from the user's personal browser, using an isolated Chrome profile.

---

## 📂 Project Structure

```
📁 Project
📌 alfa.py
📌 alfa_craigslist.py
📌 alfa_facebook.py
📌 all_listings.json
📌 extract_json_from_html.py
📌 chromedriver.exe
📌 README.md
📌 saved_pages.zip
🕛
📁 config/
📌 config.yaml          # Chrome profile configuration
📌 facebook.yaml        # Facebook Marketplace search tasks
📌 craigslist.yaml      # Craigslist config (optional)
📌 dashboard.yaml
📌 global.yaml
🕛
📁 craigslist/
📌 cl_scraper.py
📌 cl_utils.py
🕛
📁 dashboard/
📌 app.py
🕛
📁 facebook/
📌 auto_scroll.py
📌 facebook_task_extractor.py
📌 file_checker.py
📌 navigation.py
📌 search_loader.py
📌 set_location_filter.py
📌 visited_tracker.py
🕛
📁 logs/
📌 visited_urls.csv      # CSV log with URL and timestamp
📌 visited_urls.txt      # Simple URL log
🕛
📁 processed_pages/          # Saved Facebook HTML pages (excluded from installer)
📁 saved_pages/              # Other saved HTML pages
📁 session/                  # Saved cookies (optional)
```

---

## 📋 Main Features

* 🔎 **Automatic Navigation**: to Marketplace -> Vehicles -> Cars.
* 🛡️ **Advanced Filtering**: by location and price range.
* 📀 **Local Saving**: HTML + JSON extraction.
* 📝 **Smart Logging**: skips already visited listings.
* 🌐 **Separate Browser**: uses its own Chrome profile without affecting the user's browser.
* 🛠️ **Easy Installation**: delivered as a single `.exe` package.

---

## ⚙️ Setup (Quick Version)

### 1. Minimum Requirements

* 🦍 Python 3.11+ (only if running the source code; the `.exe` version does not require Python).
* Google Chrome installed on the system (any recent version).

---

### 2. Installation via Executable

**If using the `.exe` or setup installer:**

* Run `FacebookScraperSetup.exe`.
* Installation will create a Desktop shortcut.
* **Double-click** and the application will start immediately!

---

### 3. Configuration

#### 🔧 File `config/config.yaml`

Configure the isolated Chrome profile:

```yaml
active_profile: "default"

profiles:
  default:
    user_data_dir: "chrome_profile"   # Isolated profile, does not affect user's browser
    resolution: "1920,1080"           # Browser resolution
```

---

#### 🔧 File `config/facebook.yaml`

List the cities and price filters:

```yaml
search_tasks:
  - city: "New York"
    price_min: 100
    price_max: 1000

  - city: "Los Angeles"
    price_min: 500
    price_max: 5000
```

**Fields:**

* `city` — City to search ads in.
* `price_min` — Minimum price.
* `price_max` — Maximum price.

---

## 📄 Logging and Tracking

* **visited\_urls.txt** — maintains a list of all URLs already processed to avoid duplicates.
* **visited\_urls.csv** — detailed log with URL, save date, and filename.
* Logs are automatically saved in the `logs/` folder on first run.

---

## 🛠️ How to Run (Developer Mode)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the main script:

```bash
python alfa_facebook.py
```

---

## 🕹️ Packaging into .EXE

1. Make sure you have `pyinstaller` installed:

```bash
pip install pyinstaller
```

2. Build the executable:

```bash
pyinstaller --onefile \
    --add-data "chromedriver.exe;." \
    --add-data "config;config" \
    --add-data "facebook;facebook" \
    --add-data "craigslist;craigslist" \
    --add-data "logs;logs" \
    alfa_facebook.py
```

---

## 🔧 Building a Professional Installer (Optional)

You can create a friendly installer with [InnoSetup](https://jrsoftware.org/isinfo.php):

Sample `.iss` script:

```ini
[Setup]
AppName=Facebook Scraper
AppVersion=1.0
DefaultDirName={autopf}\FacebookScraper
DefaultGroupName=Facebook Scraper
OutputDir=installer
OutputBaseFilename=FacebookScraperSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\facebook_scraper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "chromedriver.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Facebook Scraper"; Filename: "{app}\facebook_scraper.exe"
Name: "{commondesktop}\Facebook Scraper"; Filename: "{app}\facebook_scraper.exe"
```

---

## 🔔 Notes

* Ensure Google Chrome is installed and updated.
* All scraping activities must respect the terms of service of the target website.
* Use this tool responsibly and ethically.
