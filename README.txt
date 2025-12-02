AutoMarketFlow – Car Market Scraper & Interactive Dashboard

Automated vehicle marketplace analyzer for Facebook Marketplace & Craigslist

📌 Overview

AutoMarketFlow is an automated workflow (not a high-speed scraper) designed to help users analyze vehicle listings from Facebook Marketplace and Craigslist.
It provides:

✔ Automated navigation
✔ Data extraction
✔ Text cleaning
✔ Vehicle filtering
✔ Interactive dashboard for browsing and analyzing results
✔ Persistent session (Facebook login saved)
✔ Zero technical skills required after installation

⚠️ This tool automates browser actions exactly like a human, respecting browser delays and avoiding aggressive scraping techniques.





Installation Video

For a step-by-step visual installation guide, you can watch this video:
  ---> https://www.youtube.com/watch?v=bMTnO_YP_Go
This short tutorial demonstrates how to install the application, configure dependencies, and complete the first-time setup.

IMPORTANT: READ BEFORE RUNNING
https://www.youtube.com/watch?v=bMTnO_YP_Go
Before you use the program, ensure that:

✅ 1. Install Google Chrome
AutoMarketFlow uses Chrome for automation.

Download Chrome:
https://www.google.com/chrome/
If Chrome is already installed → you're good.

✅ 2. Install Python 3.x
Inside the folder AutoMarket_Installer_Pack, you will find:

python-3.13.5-amd64.exe
Right-click → Run as Administrator.
During installation:
✔ Check “Add Python to PATH” (VERY important)
✅ 3. Start the installer
Double-click:
START_CLICK_HERE.bat
This script will:

Install all dependencies
Prepare the environment
Launch the dashboard
Configure the Chrome automation profile

After the dashboard opens in your browser:
➡️ You may close the browser and the command window — the installation is complete.

🔓 FIRST-TIME FACEBOOK LOGIN (REQUIRED ONCE)
After installation, run:

first_time_facebook_login.bat
This opens Chrome using the automated profile.
Log in to Facebook manually.

Your session is saved permanently.
From now on, running the main program will not require login again.

▶️ Daily Usage

Once installed, simply run:

START_CLICK_HERE.bat

The app will:
Load your saved Facebook session
Open the dashboard
Perform automated searches
Extract listings
Update your database

Display everything in the GUI dashboard

🧠 Main Features
✔ Automated Facebook Marketplace extraction

Opens Marketplace
Selects Vehicles → Cars
Applies city + radius filter
Applies min/max price
Scrolls and loads all listings
Extracts text content safely
Stores results without duplicates
✔ Craigslist integration (optional)
✔ Advanced text analysis

Owner count detection

Positive keywords scan

Auto-cleaning of spam or repetitive text

✔ Beautiful interactive dashboard

Filters by price, mileage, owners, keywords

Color-coded listings

Embedded image previews

Export to JSON

📁 Project Structure
auto_marketflow/
│
├── main.py                     # Entry point – automation workflow
│
├── config/
│   ├── config.yaml             # Chrome profile, resolution, settings
│   └── facebook.yaml           # Search cities & price ranges
│
├── scraping/
│   ├── navigation.py           # Marketplace navigation (Vehicles → Cars)
│   ├── set_location_filter.py  # City + radius filter automation
│   ├── set_price_filter.py     # Price range automation
│   ├── marketplace_extractor.py# Extractor logic
│   ├── auto_scroll.py          # Safe incremental scrolling
│   ├── file_checker.py         # Duplicate prevention
│   ├── visited_tracker.py      # Tracks processed listings
│   └── text_analyzer.py        # Keywords & owner detection
│
├── dashboard/
│   ├── gui_main.py             # Full GUI dashboard
│   ├── filters.py              # Filtering logic
│   ├── ui_assets/              # Icons / CSS / images
│   └── table_view.py           # Visual components
│
├── parsing/
│   ├── html_cleaner.py
│   ├── text_cleaner.py
│   └── json_exporter.py
│
└── utils/
    ├── logging_setup.py
    ├── helpers.py
    └── constants.py

⚠️ Legal Notice

This software automates browser actions exactly as a human user.
It:

❌ does NOT bypass Facebook security
❌ does NOT gather private data
❌ does NOT access API endpoints
❌ does NOT perform high-speed scraping

✔ It only automates clicks, scrolls, and page reading using the same Chrome interface a human would use.

Usage is at your own responsibility.
Make sure your use complies with platform terms and local laws.

🤝 Contributing

Pull requests and improvements are welcome.
https://vorte.eu/contact
📧 Support
For installation help or feature requests, open an Issue in the repo.


