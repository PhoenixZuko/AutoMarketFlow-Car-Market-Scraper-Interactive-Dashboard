import json
import re
import os
from datetime import datetime, timedelta

def convert_listed_since_to_hours_string(listed_since, scraped_date):
    if not listed_since:
        return listed_since

    listed_since = listed_since.replace("about ", "").replace("approximately ", "").strip()

    # Încearcă să parsezi scraped_date, altfel folosește datetime.now()
    try:
        scraped_dt = datetime.strptime(scraped_date, "%Y-%m-%d %H:%M")
    except Exception:
        scraped_dt = datetime.now()

    delta = None
    if re.match(r"\d+\s+year", listed_since):
        delta = timedelta(days=int(re.findall(r"\d+", listed_since)[0]) * 365)
    elif re.match(r"\d+\s+week", listed_since):
        delta = timedelta(weeks=int(re.findall(r"\d+", listed_since)[0]))
    elif re.match(r"\d+\s+day", listed_since):
        delta = timedelta(days=int(re.findall(r"\d+", listed_since)[0]))
    elif re.match(r"\d+\s+hour", listed_since):
        delta = timedelta(hours=int(re.findall(r"\d+", listed_since)[0]))
    elif re.match(r"\d+\s+minute", listed_since):
        delta = timedelta(minutes=int(re.findall(r"\d+", listed_since)[0]))
    elif "a year ago" in listed_since:
        delta = timedelta(days=365)
    elif "a week ago" in listed_since:
        delta = timedelta(weeks=1)
    elif "a day ago" in listed_since:
        delta = timedelta(days=1)
    elif "an hour ago" in listed_since:
        delta = timedelta(hours=1)
    elif "a minute ago" in listed_since:
        delta = timedelta(minutes=1)

    if delta is None:
        return listed_since

    posted_at = scraped_dt - delta
    now = datetime.now()
    hours_since_posted = round((now - posted_at).total_seconds() / 3600, 2)
    return str(int(round(hours_since_posted)))


    posted_at = scraped_dt - delta
    now = datetime.now()
    hours_since_posted = round((now - posted_at).total_seconds() / 3600, 2)
    return str(int(round(hours_since_posted)))

def convert_craigslist_to_standard():
    input_path = os.path.join("craig_script_json", "craig_with_flags_final.json")
    output_dir = os.path.join(".", "tubulator_display")
    os.makedirs(output_dir, exist_ok=True)
    intermediate_file = os.path.join(output_dir, "cars_tabulator_craig.json")
    final_output_file = os.path.join(output_dir, "cars_tabulator.json")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(f"[EROARE] Fisierul de intrare nu a fost gasit: {e}")
        return

    output = []
    for item in data:
        try:
            raw_title = item.get("title", "")
            seller_type = "unknown"

            match = re.search(r"for sale by (owner|dealer)", raw_title.lower())
            if match:
                seller_type = match.group(1)

            title_clean = re.sub(r"\s*for sale by.*", "", raw_title).strip()
            title_clean = re.sub(r"\s*-\s*.*$", "", title_clean).strip()

            brand = item.get("make")
            if not brand:
                match = re.search(r'\b(19|20)\d{2}\b\s+(\w+)', title_clean)
                if match:
                    brand = match.group(2).capitalize()

            since = convert_listed_since_to_hours_string(item.get("listed_since"), item.get("scraped_date", ""))

            new_entry = {
                "id": item.get("id"),
                "title": title_clean,
                "price": f'{item.get("price", "")} $',
                "year": item.get("year"),
                "Brand": brand,
                "mileage": item.get("mileage"),
                "fuel": (item.get("fuel_type") or "")[:3],
                "Tra": (item.get("transmission") or "")[:3],
                "type": item.get("extra_craig", {}).get("type"),
                "seller": seller_type,
                "city": item.get("location", {}).get("city"),
                "state": item.get("location", {}).get("state"),
                "vin": item.get("vin"),
                "ext_col": item.get("exterior_color"),
                "int_col": item.get("interior_color"),
                "own": item.get("owner_count"),
                "safety": item.get("nhtsa_safety_rating"),
                "paid": item.get("paid_off"),
                "rating": item.get("seller", {}).get("rating"),
                "joined": item.get("seller", {}).get("joined_facebook"),
                "since": since,
                "score": item.get("car_score"),
                "pflags": item.get("positive_flags"),
                "nflags": item.get("negative_flags"),
                "sscore": item.get("seller_score"),
                "clean": item.get("has_clean_title"),
                "has_vin": item.get("has_vin"),
                "url": item.get("extra_craig", {}).get("url", "").replace("URL: ", "").strip()
            }
            output.append(new_entry)
        except Exception as e:
            print(f"[ATENTIE] Eroare la procesarea unui obiect: {e}")

    # Salvăm temporar primul fișier
    try:
        with open(intermediate_file, 'w', encoding='utf-8') as out_f:
            json.dump(output, out_f, indent=2, ensure_ascii=False)
        print(f"[INFO] Fisier intermediar salvat: {intermediate_file}")
    except Exception as e:
        print(f"[EROARE] Salvare fișier intermediar eșuată: {e}")
        return

    # Verificăm dacă mai există alt json în folder și concatenăm
    try:
        all_data = []
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if filename.endswith(".json") and filename != "cars_tabulator.json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    all_data.extend(content)

        with open(final_output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Concatenare completă în: {final_output_file}")
    except Exception as e:
        print(f"[EROARE] Eroare la concatenare: {e}")

if __name__ == "__main__":
    convert_craigslist_to_standard()
