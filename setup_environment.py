import os
import sys
import subprocess
import shutil

# === Setup environment variables to force correct ChromeDriver ===
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

# === Step 1: Install webdriver-manager FIRST ===
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("📦 'webdriver-manager' not found. Installing it first...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
    from webdriver_manager.chrome import ChromeDriverManager

# === Step 2: Install all other required modules ===
modules = ["flask", "psutil", "pyyaml", "bs4", "selenium"]
print("\n📦 [Module Setup] Checking and installing required Python packages...\n")
for module in modules:
    try:
        __import__(module.replace("-", "_"))
        print(f"✅ {module} is already installed.")
    except ImportError:
        print(f"📥 Installing {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# === Step 3: Download correct ChromeDriver version ===
target_path = r"C:\chromedriver\chromedriver.exe"
print(f"\n🔧 [ChromeDriver] Checking if ChromeDriver exists at {target_path}...")

if os.path.exists(target_path):
    print("🧹 Deleting outdated ChromeDriver to ensure correct version is downloaded...")
    try:
        os.remove(target_path)
        print("✅ Old ChromeDriver removed.")
    except Exception as e:
        print(f"❌ Failed to delete old ChromeDriver: {e}")
        sys.exit(1)

try:
    print("⬇️  Downloading matching ChromeDriver for your browser...")
    downloaded_path = ChromeDriverManager().install()
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copy(downloaded_path, target_path)
    print(f"✅ ChromeDriver installed at: {target_path}")
except Exception as e:
    print(f"❌ Failed to install ChromeDriver: {e}")
    sys.exit(1)

# === Step 4: Ensure Chrome profile exists ===
chrome_profile_path = r"C:\FB_Profile_HD\Default\Preferences"
if not os.path.exists(chrome_profile_path):
    print(f"\n⚠️  Chrome profile not found at {chrome_profile_path}. Creating minimal structure...")
    os.makedirs(os.path.dirname(chrome_profile_path), exist_ok=True)
    with open(chrome_profile_path, "w", encoding="utf-8") as f:
        f.write("{}")
    print("✅ Empty Chrome profile created.")
else:
    print("✅ Chrome profile already exists.")

print("\n🎉 Environment is fully ready. Returning to launcher...\n")
