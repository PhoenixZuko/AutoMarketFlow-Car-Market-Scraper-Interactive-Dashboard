from datetime import datetime
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from facebook.visited_tracker import VisitedTracker
from facebook.navigation import navigate_to_marketplace_vehicles_cars
from facebook.set_location_filter import set_location_filter, set_price_filter
from facebook.file_checker import is_file_in_database

def run_marketplace_extraction(driver, search_task):
    tracker = VisitedTracker()
    wait = WebDriverWait(driver, 20)

    city = search_task.get("city")
    price_min = search_task.get("price_min")
    price_max = search_task.get("price_max")

    if not navigate_to_marketplace_vehicles_cars(driver):
        print("❌ Navigation failed. Exiting.")
        return

    set_location_filter(driver, wait, city)
    set_price_filter(driver, wait, price_min, price_max)

    print("[Step 4] Collecting all listings...")
    listings = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")
    print(f"ℹ️ Found {len(listings)} listings.")

    skipped_files = 0
    saved_files = 0

    for index, listing in enumerate(listings):
        print(f"[🔁] Processing listing {index + 1}/{len(listings)}")

        try:
            listing_url = listing.get_attribute("href")
            if not listing_url:
                print(f"❌ No URL found for listing {index + 1}. Skipping.")
                continue

            filename_base = listing_url.split("/")[-2]
            txt_filename = f"{filename_base}.txt"

            if is_file_in_database(f"{filename_base}.html"):  # încă verificăm baza de date pe baza .html
                print(f"⏭️ Listing {filename_base} already in database. Skipping.")
                skipped_files += 1
                continue

            driver.execute_script("arguments[0].scrollIntoView();", listing)
            time.sleep(1)
            listing.click()
            time.sleep(7)

            # Click 'See more' if available
            try:
                see_more = driver.find_element(By.XPATH, "//span[text()='See more']")
                see_more.click()
                time.sleep(7)
            except NoSuchElementException:
                print("ℹ️ 'See more' not found, continuing.")

            # Salvăm doar textul (nu HTML)
            full_text = driver.find_element(By.TAG_NAME, "body").text

            os.makedirs("saved_pages", exist_ok=True)
            filepath_txt = os.path.join("saved_pages", txt_filename)

            with open(filepath_txt, "w", encoding="utf-8") as f_txt:
                f_txt.write(full_text)

            print(f"✅ Text saved to {filepath_txt} (HTML not saved)")
            tracker.mark_visited(listing_url, filename=f"{filename_base}.html")
            saved_files += 1

        except (IndexError, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"❌ Could not open listing {index + 1}: {e}")
            continue

        print("↩️ Going back to listings page...")
        driver.back()
        time.sleep(7)

        # Refresh listings after going back
        listings = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")

    print(f"✅ All listings processed. {saved_files} new saved, {skipped_files} skipped (already in database).")
