# 🚀 Facebook Marketplace Scraper — Installation Guide

Welcome! Follow the instructions below to install and run the scraper.

---

## 📚 Requirements
- ✅ **Python 3.11 or newer** (Download: https://www.python.org/downloads/)
  > **IMPORTANT**: During installation, make sure to check "**Add Python to PATH**."
- ✅ **Google Chrome** installed (Download: https://www.google.com/chrome/)
- ✅ **Internet Connection**

---

## 📦 Project Structure



FacebookScraper/
├── chromedriver.exe # Chrome WebDriver
├── first_run.py # First-time profile setup
├── alfa_facebook.py # Main scraping script
├── install_and_run.bat # Setup and launcher
├── requirements.txt # Python libraries
├── INSTALL.md # Installation instructions
├── README.md # About the project
│
├── config/ # Configuration files (YAML)
├── facebook/ # Scraper modules
├── logs/ (empty folder) # Visit logs



---

## 🛠️ Installation Steps

### 1. Unzip the Folder
Extract the provided `.zip` file to a folder of your choice.

### 2. Run the Setup
Double-click `install_and_run.bat` and follow the instructions:

- It will check if Python is installed.
- It will check if `chromedriver.exe` is in place.
- It will install the required Python libraries.
- It will detect if this is the **first run**:
  - If so, it will open a Chrome browser window.
  - **Manually log in to Facebook** in the opened window.
  - Press **ENTER** in the console once you're logged in.
  - The session will be saved — no login will be required next time.

### 3. Run the Scraper
After the first setup:
- Simply double-click `install_and_run.bat` to start scraping.
- The script will use the saved login session automatically.

---

## 🧩 Important Notes
- **ChromeDriver** must match the installed Chrome version.
- **Your Facebook account must be active** and not blocked.
- **Profile Data** is saved locally in the `chrome_profile/` folder.
- **No personal browser data is touched** — this scraper uses an independent profile.

---

## ❓ Troubleshooting
- If you see `chromedriver.exe not found` — make sure the file is in the same folder as the `.bat` file.
- If you see `Python is not installed` — download and install Python 3.11+, and **check Add to PATH** during setup.

---

## 📬 Contact
For any issues or help, please contact [your_email@example.com].



# 🚀 Facebook Marketplace Scraper — Installation Guide

Welcome! Follow the instructions below to install and run the scraper.

---

## 📚 Requirements
- ✅ **Python 3.11 or newer** (Download: https://www.python.org/downloads/)
  > **IMPORTANT**: During installation, check "**Add Python to PATH**."
- ✅ **Google Chrome** installed (Download: https://www.google.com/chrome/)

> **If Python and Chrome are already installed, you can skip this step.**

---

## 🛠️ HOW TO INSTALL

1. Unzip the folder to a location of your choice.

2. Double-click `install_and_run.bat`.

3. On first run:
   - A clean Chrome window will open.
   - Log in manually to Facebook.
   - After logging in, return to the console and press ENTER.

✅ Next time: just double-click and scrape — no login needed!

---

## 🔒 Important Information

- The program uses the **Chrome browser installed** on your computer.
- It creates a **separate Chrome profile** — it does **NOT** touch your personal Chrome data (passwords, history, saved sessions).
- On the **first run**, you need to log in manually to Facebook.
- ✅ After the first login, your session will be saved automatically.
- **From the next run**, login is automatic — no manual login required!

> **Your personal Chrome browser remains safe and untouched.**

---

## ❓ Troubleshooting

- **Python not found** — Make sure Python is installed and "Add Python to PATH" was selected.
- **ChromeDriver not found** — Ensure `chromedriver.exe` is in the same folder as `install_and_run.bat`.
- **Browser not opening** — Ensure Google Chrome is properly installed and updated.

---

## 📬 Contact
For any issues or help, please contact: [your_email@example.com]

🔧 IMPORTANT:

- Google Chrome must be installed in the **default location**.
- Typically:
  - On Windows 11/10: `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - Or: `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
  
- ✅ If you installed Chrome normally, you don't need to change anything.

⚠️ If Chrome is installed in a custom location, please reinstall it in the default location or contact support.
