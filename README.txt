# AutoMarketFlow

Local-first automation and marketplace analysis platform for Facebook Marketplace and Craigslist.

The platform combines controlled browser automation, ETL-style processing, semantic filtering, and a lightweight dashboard for analyzing vehicle listings in real time.

---

## Features

- Browser automation using Selenium
- Facebook Marketplace & Craigslist workflows
- Local-only execution (no cloud infrastructure)
- Persistent Chrome sessions
- Real-time dashboard
- Vehicle filtering & semantic analysis
- Duplicate prevention & visited tracking
- YAML-driven configuration
- Process-safe execution
- Windows 11 optimized

---

## Technology Stack

### Backend & Automation
- Python
- Selenium
- Flask
- YAML configuration
- ETL workflows

### Frontend & Dashboard
- Flask templates
- HTML / CSS / JavaScript
- Tabulator.js

### System Integration
- Windows 11
- Process management
- Local browser orchestration
- Persistent Chrome profiles

---

## Architecture Overview

```text
Browser Automation
        ↓
Data Extraction
        ↓
ETL Processing
        ↓
Classification & Analysis
        ↓
Dashboard Visualization
```

---

## Main Capabilities

- automated listing extraction
- configurable search filters
- semantic text analysis
- persistent login sessions
- real-time monitoring dashboard
- safe concurrent execution
- local-only processing

---

## Demo Videos

### Full Presentation
https://www.youtube.com/watch?v=r5iQPuOCLUc

### YAML Configuration
https://www.youtube.com/watch?v=ir-ZJZGxOIQ

### Installation Guide
https://www.youtube.com/watch?v=bMTnO_YP_Go

---

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Application

```bash
python main.py
```

---

## Repository Structure

```text
auto_marketflow/
│
├── main.py
├── config/
├── scraping/
├── dashboard/
├── parsing/
├── utils/
└── templates/
```

---

## Documentation

Additional technical documentation is available inside the `DOCUMENTATION/` folder.

Included topics:
- installation
- YAML configuration
- dashboard usage
- ETL workflow
- troubleshooting
- architecture notes

---

## Legal Notice

This software automates browser interaction through standard Chrome automation workflows and does not bypass platform security mechanisms or private APIs.

Users remain responsible for complying with platform terms and applicable local laws.

---

## Author

Andrei Sorin Stefan

Backend • Automation • ETL • Infrastructure Engineering
