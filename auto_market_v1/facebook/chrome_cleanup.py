from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def close_restore_tabs_if_present(driver):
    print("🔍 Verificăm dacă există Restore Tabs...")

    try:
        # Așteptăm puțin să se încarce
        driver.implicitly_wait(3)

        # Caută elementul de Restore Tabs (în funcție de cum apare la tine, putem ajusta selectorul)
        restore_button = driver.find_element(By.XPATH, '//button[contains(text(), "Restore")]')

        if restore_button:
            print("🛑 Găsit Restore Tabs! Îl închidem...")
            restore_button.click()
            print("✅ Restore Tabs închis cu succes.")
    except NoSuchElementException:
        print("✅ Nu există mesaj Restore Tabs. Continuăm normal...")
    except Exception as e:
        print(f"⚠️ Eroare la închiderea Restore Tabs: {e}")
