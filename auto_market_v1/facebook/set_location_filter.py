from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def set_location_filter(driver, wait, city):
    try:
        print(f"[Filter] Opening location popup...")

        # 1. Click on the wrapper containing location text
        location_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'x78zum5') and contains(@class,'xl56j7k') "
            "and contains(@class,'x1y1aw1k') and contains(@class,'xf159sx') "
            "and contains(@class,'xwib8y2') and contains(@class,'xmzvs34')]"
        )))
        driver.execute_script("arguments[0].click();", location_btn)
        time.sleep(1.5)

        print("[Filter] Typing city...")

        # 2. Input field inside popup
        location_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@aria-label='Location']"
        )))

        driver.execute_script("arguments[0].value='';", location_input)
        location_input.send_keys(Keys.CONTROL + "a")
        location_input.send_keys(Keys.DELETE)
        location_input.send_keys(city)
        time.sleep(1.5)

        # 3. Select first suggestion
        location_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        location_input.send_keys(Keys.ENTER)
        time.sleep(1.5)

        print("[Filter] Applying location...")

        # 4. Click Apply in popup
        apply_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//span[normalize-space()='Apply' or normalize-space()='Aplică']/ancestor::div[@role='button']"
        )))
        driver.execute_script("arguments[0].click();", apply_btn)
        time.sleep(2)

        print("✅ Location filter applied successfully.")

    except Exception as e:
        print(f"❌ Error applying location filter: {e}")


    except Exception as e:
        print(f"❌ Location filter failed: {e}")

def set_price_filter(driver, wait, price_min, price_max):
    try:
        print(f"[Filter] Setting price range: {price_min} - {price_max}...")

        inputs = wait.until(lambda d: len(d.find_elements(By.XPATH, "//input[@placeholder='Min' or @placeholder='Max']")) >= 2)
        inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Min' or @placeholder='Max']")

        min_input = inputs[0]
        max_input = inputs[1]

        driver.execute_script("arguments[0].focus();", min_input)
        min_input.click()
        min_input.clear()
        min_input.send_keys(str(price_min))
        min_input.send_keys(Keys.TAB)
        time.sleep(0.5)

        driver.execute_script("arguments[0].focus();", max_input)
        max_input.click()
        max_input.clear()
        max_input.send_keys(str(price_max))
        time.sleep(0.5)

        max_input.send_keys(Keys.RETURN)
        time.sleep(5)

        print("✅ Price filter applied successfully.")

    except Exception as e:
        print(f"❌ Price filter failed: {e}")
