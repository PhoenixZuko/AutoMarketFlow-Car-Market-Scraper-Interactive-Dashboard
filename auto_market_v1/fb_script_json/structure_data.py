import json
import re
import os

def extract_year_make_model(title):
    if not isinstance(title, str):
        title = ""
    year_match = re.search(r'\b(19|20)\d{2}\b', title)
    year = int(year_match.group(0)) if year_match else None
    if year:
        title = title.replace(str(year), "").strip()
    words = title.split()
    make = words[0] if len(words) > 0 else None
    model = ' '.join(words[1:]) if len(words) > 1 else None
    return year, make, model

def extract_mileage(text):
    match = re.search(r'Driven ([\d,]+) miles', text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def extract_transmission(text):
    if 'Manual transmission' in text:
        return 'Manual'
    if 'Automatic transmission' in text:
        return 'Automatic'
    return None

def extract_fuel_type(text):
    match = re.search(r'Fuel type: (.+)', text)
    if match:
        return match.group(1).strip()
    return None

def extract_owner_count(text):
    match = re.search(r'(\d+)\+?\s*owners?', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def extract_colors(text):
    exterior = None
    interior = None
    exterior_match = re.search(r'Exterior color:\s*([^·\n]*)', text)
    if exterior_match:
        exterior = exterior_match.group(1).strip() or None
    interior_match = re.search(r'Interior color:\s*([^·\n]*)', text)
    if interior_match:
        interior = interior_match.group(1).strip() or None
    return exterior, interior

def extract_nhtsa_rating(text):
    if 'NHTSA' in text and 'rating' in text.lower():
        match = re.search(r'(\d)/5', text)
        if match:
            return int(match.group(1))
    return None

def extract_paid_off(text):
    if text:
        if re.search(r'\bnot paid off\b', text, re.IGNORECASE):
            return "No"
        if re.search(r'\bpaid off\b', text, re.IGNORECASE):
            return "Yes"
    return "Unknown"

def extract_vin(text):
    if not isinstance(text, str):
        return None
    match = re.search(r'\b([A-HJ-NPR-Z0-9]{17})\b', text.upper())
    if match:
        vin_candidate = match.group(1)
        if len(vin_candidate) == 17:
            return vin_candidate
    return None

def main():
    # Salvează fișierul local, în același director unde rulează scriptul
    output_path = os.path.join(os.getcwd(), "fb_structure.json")

    # Creează folderul dacă nu există
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load data
    with open('fb_script_json/all_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Încarcă datele existente dacă există
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_ids = set(entry['id'] for entry in existing_data)
    initial_id_count = len(existing_ids)

    output_data = existing_data.copy()

    for idx, entry in enumerate(data, 1):
        if entry.get('id') in existing_ids:
            continue

        seller_info = entry.get("seller_information", {})

        new_entry = {
            "id": entry.get("id"),
            "title": entry.get("title"),
            "price": entry.get("price"),
            "currency": entry.get("currency"),
            "location": entry.get("location"),
            "year": None,
            "make": None,
            "model": None,
            "mileage": None,
            "transmission": None,
            "fuel_type": None,
            "owner_count": None,
            "exterior_color": None,
            "interior_color": None,
            "nhtsa_safety_rating": None,
            "paid_off": "Unknown",
            "vin": None,
            "seller": {
                "name": seller_info.get("name"),
                "rating": seller_info.get("rating"),
                "joined_facebook": seller_info.get("joined_facebook"),
                "description": {}
            },
            "listed_since": entry.get("listed_since"),
            "scraped_date": entry.get("scraped_date"),
            "internal_id": entry.get("internal_id"),  # <-- AICI
            "raw_details": {},
        }

        year, make, model = extract_year_make_model(entry.get("title", ""))
        new_entry["year"] = year
        new_entry["make"] = make
        new_entry["model"] = model

        details = entry.get("vehicle_details", {}).get("details", {})
        remaining_details = {}

        for k, v in details.items():
            used = False

            if new_entry["mileage"] is None:
                mileage = extract_mileage(v)
                if mileage is not None:
                    new_entry["mileage"] = mileage
                    used = True

            if new_entry["transmission"] is None:
                trans = extract_transmission(v)
                if trans:
                    new_entry["transmission"] = trans
                    used = True

            if new_entry["fuel_type"] is None:
                fuel = extract_fuel_type(v)
                if fuel:
                    new_entry["fuel_type"] = fuel
                    used = True

            if new_entry["exterior_color"] is None or new_entry["interior_color"] is None:
                exterior, interior = extract_colors(v)
                if exterior or interior:
                    new_entry["exterior_color"] = exterior or new_entry["exterior_color"]
                    new_entry["interior_color"] = interior or new_entry["interior_color"]
                    used = True

            if new_entry["nhtsa_safety_rating"] is None:
                rating = extract_nhtsa_rating(v)
                if rating:
                    new_entry["nhtsa_safety_rating"] = rating
                    used = True

            if new_entry["paid_off"] == "Unknown":
                paid_status = extract_paid_off(v)
                if paid_status == "Yes":
                    new_entry["paid_off"] = True
                    used = True
                elif paid_status == "No":
                    new_entry["paid_off"] = False
                    used = True

            if not used:
                remaining_details[k] = v

        if new_entry["owner_count"] is None:
            for k, v in list(remaining_details.items()):
                owner = extract_owner_count(v)
                if owner is not None:
                    new_entry["owner_count"] = owner
                    del remaining_details[k]
                    break

        seller_desc = entry.get("seller_description", {})

        for idx_desc, (k, v) in enumerate(seller_desc.items(), 1):
            if v.strip().lower() != "see translation":
                if new_entry.get("vin") is None:
                    detected_vin = extract_vin(v)
                    if detected_vin:
                        new_entry["vin"] = detected_vin
                new_entry["seller"][f"seller_description_{idx_desc}"] = v

        for idx_rem, (k, v) in enumerate(remaining_details.items(), 1):
            new_entry["raw_details"][f"vehicle_details_{idx_rem}"] = v

        output_data.append(new_entry)
        existing_ids.add(new_entry['id'])

        if idx % 10 == 0 or idx == len(data):
            print(f"Processed {idx}/{len(data)} entries...")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    new_entries_added = len(existing_ids) - initial_id_count

    if new_entries_added == 0:
        print(f"ℹ️ Nicio intrare nouă adăugată. Totul e deja actualizat. Total entries: {len(output_data)}.")
    else:
        print(f"✅ Added {new_entries_added} new entries. Total entries now: {len(output_data)}.")

    print(f"✅ Saved in {output_path}")
    print(f"✅ Finished processing {len(output_data)} entries. Saved in {output_path}")

if __name__ == "__main__":
    main()
