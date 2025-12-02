import time
from selenium.webdriver.common.by import By

def auto_scroll_until_no_new(driver, pause_time=3, max_no_change=2):
    """
    Scrolls progressively until no new listings are loaded after several attempts.
    
    :param driver: Selenium WebDriver
    :param pause_time: Time to wait after each scroll (in seconds)
    :param max_no_change: How many scrolls with no new listings before stopping
    """
    print("🚀 Starting progressive auto-scroll...")

    last_count = 0
    no_change_count = 0
    total_scrolls = 0

    while True:
        # Numărăm anunțurile curente
        listings = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")
        current_count = len(listings)

        print(f"📜 Scroll {total_scrolls + 1}: {current_count} listings found.")

        if current_count == last_count:
            no_change_count += 1
            print(f"⚠️ No new listings detected ({no_change_count}/{max_no_change}).")
        else:
            no_change_count = 0  # Reset dacă au apărut noi anunțuri

        if no_change_count >= max_no_change:
            print("✅ No more new listings loaded after multiple scrolls. Stopping.")
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        last_count = current_count
        total_scrolls += 1

    print(f"🛑 Scrolling finished after {total_scrolls} scrolls.")
