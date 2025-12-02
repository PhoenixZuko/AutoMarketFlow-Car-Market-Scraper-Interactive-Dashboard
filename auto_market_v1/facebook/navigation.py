import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def navigate_to_marketplace_vehicles_cars(driver):
    print("[Step 1] Navigating to Marketplace...")
    driver.get("https://www.facebook.com/marketplace")
    time.sleep(6)

    print("[Step 2] Opening Vehicles category...")

    # 1️⃣ Găsim orice element relevant pentru Vehicles
    vehicles_selectors = [
        "//a[contains(@href, '/marketplace/category/vehicles')]",
        "//div[@role='link' and contains(@aria-label, 'Vehicles')]",
        "//span[text()='Vehicles' or text()='Vehicule']"
    ]

    vehicles_button = None
    for selector in vehicles_selectors:
        try:
            vehicles_button = driver.find_element(By.XPATH, selector)
            break
        except:
            pass

    if not vehicles_button:
        print("❌ 'Vehicles' category not found. UI changed.")
        return False

    driver.execute_script("arguments[0].click();", vehicles_button)
    time.sleep(5)

    print("[Step 3] Selecting Cars / Cars & Trucks...")

    subcategory_selectors = [
        "//a[contains(@href, '/marketplace/category/vehicles/cars')]",
        "//a[contains(@href, '/marketplace/category/vehicles/cars-trucks')]",
        "//div[@role='link' and contains(@aria-label,'Cars')]",
        "//span[contains(text(),'Cars')]",
        "//span[contains(text(),'Trucks')]",
    ]

    cars_button = None
    for selector in subcategory_selectors:
        try:
            cars_button = driver.find_element(By.XPATH, selector)
            break
        except:
            pass

    if not cars_button:
        print("❌ Cars/Cars & Trucks subcategory NOT found.")
        return False

    driver.execute_script("arguments[0].click();", cars_button)
    time.sleep(5)

    print("✅ Vehicles → Cars navigation successful.")
    return True
