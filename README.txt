Video & Tutorials
 Full Presentation — Project Overview
A complete walkthrough covering architecture, features, workflow, and real usage:
👉 https://www.youtube.com/watch?v=r5iQPuOCLUc

 Quick Usage Guide (YAML Configuration)
How to set location and price ranges directly through the YAML configuration file:
👉 https://www.youtube.com/watch?v=ir-ZJZGxOIQ

 Installation Guide — Step-by-Step
A short tutorial showing the installation process, dependency setup, and first-time initialization:
👉 https://www.youtube.com/watch?v=bMTnO_YP_Go

📬 Contact
For usage requests, technical questions, or collaboration opportunities, feel free to reach out:
 https://vorte.eu/contact

📝 Project Overview & Technical Background

This application was developed for a small automotive company that specialized in sourcing and reselling used vehicles. A core part of their workflow involved monitoring online marketplaces and identifying valuable listings quickly and accurately. To support this process, a dedicated automation system was designed to run locally on the client’s workstation, ensuring both performance and data privacy.
The solution integrates several controlled components working together as a unified flow:
✔ Local-Only Execution (No Cloud Dependencies)
The entire system operates on the user’s laptop, using a controlled Chrome profile, local storage, and a custom dashboard.
This eliminates external dependencies and ensures predictable performance in a closed environment.

✔ Automated Browser-Based Workflow
A Selenium-driven engine handles real-time interaction with Facebook Marketplace, including:
navigation through categories
setting filters (location, radius, price, etc.)
scrolling and dynamic content loading
extracting listing details
monitoring page state and detecting UI changes
All actions remain fully visible in the browser, as requested by the client.

✔ Interactive Dashboard & Control Panel

A custom local dashboard provides:
manual control (Start / Stop Automation)
configuration inputs (keywords, filters, thresholds)
active status monitoring
live listing view with sorting and filtering
The dashboard communicates with the automation engine through local processes, enabling safe and synchronized control.

✔ Text Processing & Semantic Analysis
A built-in analysis module evaluates each listing using:
positive keyword detection (clean title, good condition, new tires, etc.)
price and mileage validation
anomaly scoring
These heuristics help isolate the most relevant vehicle listings for the client's business needs.

✔ Process Monitoring & Safe Execution

Because the program needed to run alongside other business applications, the system includes safeguards for:
tracking active process IDs
preventing interference with unrelated software
controlled shutdown of only the automation-related instances
persistent Chrome session handling (login saved locally)
This ensures robust operation even during prolonged or repeated use.

✔ Windows 11 Optimized

The solution was developed, tested, and validated exclusively on Windows 11, ensuring compatibility with:
Chrome automation
file system paths
process management

Python runtime and dependencies


AutoMarketFlow – Car Market Scraper & Interactive Dashboard
Automated vehicle marketplace analyzer for Facebook Marketplace & Craigslist
 Overview
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



Quick Tutorial (YAML Configuration)
A short tutorial explaining how to configure location and price range directly through the YAML settings is available here:

Video & Tutorials
Full presentation (overview of the project + features + workflow):
https://www.youtube.com/watch?v=r5iQPuOCLUc
Quick usage guide (how to configure location and price filters via YAML):
https://www.youtube.com/watch?v=ir-ZJZGxOIQ

The video shows only the essentials:


Technical Overview

AutoMarketFlow is built as a local automation and data-processing workflow.
It combines controlled browser automation with an ETL-style pipeline and a lightweight backend that manages multiple processes safely.

The system was designed specifically for Windows 11 and uses a persistent Chrome profile, a Flask dashboard, and a multi-stage extraction engine to analyze vehicle listings in real time.

🔧 Core Capabilities (Short Technical Summary)

ETL pipeline (Extract → Transform → Load)
Browser automation through Selenium + ChromeDriver
Process monitoring (PID tracking, safe shutdown)
Local port-based separation (Flask UI on port 5000, automation isolated)
Real-time dashboard for control, filters, and data browsing
Keyword-based semantic analysis (positive/negative indicators)
Owner detection + vehicle text classification
Automatic environment setup through batch scripts
Persistent login session using a dedicated Chrome profile
Safe concurrent execution with other applications running on the same machine

🛠 Technologies Used
Backend & Automation

Python 3.x
Selenium WebDriver
ChromeDriver
Custom Chrome user-data profile
Process / PID management
Batch automation scripts (Windows .bat)

Dashboard & UI
Flask (local web server)
HTML templates
CSS (basic UI styling)
JavaScript (interactive elements)
Data Processing
Custom ETL pipeline
Regex-based text parsing
Keyword classification engine
JSON export module
Deduplication + visited tracker
File-based storage
System Integration

Windows 11 optimized execution
Port binding (Flask on 5000)
Automated dependency installation (pip)
Safe start/stop orchestration
Multi-process coordination



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
 Project Structure
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

 
C:.
│   .gitignore
│   dasboard.py
│   first_time_facebook_login.bat
│   README.txt
│   requirements.txt
│   setup_environment.py
│   START_CLICK_HERE.bat
│   sumary_readME.txt
│
├───auto_market_v1
│   │   alfa_craigslist.py
│   │   alfa_facebook.py
│   │   config.yaml
│   │   config_seller.yaml
│   │   craiglist_pid.txt
│   │   craig_extract_json.py
│   │   fb_extract_json.py
│   │   INSTALL.md
│   │   login_first_time.py
│   │   program_pid.txt
│   │   requirements.txt
│   │
│   ├───config
│   │   │   config.yaml
│   │   │   craigslist.yaml
│   │   │   facebook.yaml
│   │   │
│   │   └───yaml_generator
│   │       │   craigslist_yaml_generator.py
│   │       │   craig_config_writer.py
│   │       │   fb_config_writer.py
│   │       │   fb_yaml_generator.py
│   │       │
│   │       └───data
│   │               craig_form_data.json
│   │               fb_form_data.json
│   │               state_city_clean.json
│   │
│   ├───craigslist
│   │       scraper.py
│   │
│   ├───craig_script_json
│   │       cars_tabulator.py
│   │       converted_craiglist_with_extras.json
│   │       convert_craigslist_to_standard.py
│   │       convert_flags_for_craig.py
│   │       craiglist_clean_json.json
│   │       craiglist_json.json
│   │       craig_clean_json.py
│   │       craig_with_flags_final.json
│   │       update_tabulator_data.py
│   │       __init__.py
│   │
│   ├───dashboard_craiglist
│   │       craiglist_pid.txt
│   │       program_pid.txt
│   │       start_craiglist.py
│   │       start_extract_json_craiglist.py
│   │       start_generate_yaml_craig.py
│   │       stop_craiglist.py
│   │
│   ├───dashboard_facebook
│   │       cmd_pid.txt
│   │       program_pid.txt
│   │       start_extract_json.py
│   │       start_faceboock.py
│   │       start_generator_yaml_fb.py
│   │       stop_facebook.py
│   │
│   ├───facebook
│   │       auto_scroll.py
│   │       chrome_cleanup.py
│   │       clean_session.py
│   │       facebook_task_extractor.py
│   │       file_checker.py
│   │       navigation.py
│   │       search_loader.py
│   │       set_location_filter.py
│   │       visited_tracker.py
│   │
│   ├───fb_script_json
│   │       all_data.json
│   │       calculate_rating_seller.py
│   │       clean_emoticone.py
│   │       config.yaml
│   │       config_seller.yaml
│   │       positive_flags.py
│   │       rating_json.py
│   │       structure_data.py
│   │       tubulator.py
│   │
│   └───tubulator_display
│           cars_tabulator.json
│           cars_tabulator_craig.json
│           cars_tabulator_fb.json
│           update_tabulator_data.py
│
├───display
│   │   display.py
│   │   routes.py
│   │
│   ├───data
│   │       cars_tabulator.json
│   │       cars_tabulator_temp.json
│   │
│   ├───static
│   │   └───media
│   │       ├───css
│   │       │       datatables.min.css
│   │       │       jquery.dataTables.min.css
│   │       │       tabulator.min.css
│   │       │
│   │       └───js
│   │               jquery.min.js
│   │               tabulator.min.js
│   │
│   ├───templates
│   │   │   index.html
│   │   │
│   │   └───partials
│   │           table.html
│   │
│   └───utils
│           cars.json
│           processor.py
│
└───templates
        index.html


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


