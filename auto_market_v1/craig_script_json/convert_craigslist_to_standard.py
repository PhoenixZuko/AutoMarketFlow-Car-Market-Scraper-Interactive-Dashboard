import json
import os
from datetime import datetime

output_file = os.path.join(os.getcwd(), "converted_craiglist_with_extras.json")

def convert_craiglist_to_fb_format(craiglist_data):
    converted_list = []

    for entry in craiglist_data:
        vehicle = entry.get("vehicle", {})
        seller_descriptions = []
        extra = {}

        # Description în bloc
        description_text = entry.get("customer_title_description", "")
        if isinstance(description_text, str):
            seller_descriptions = [line.strip() for line in description_text.strip().split("\n") if line.strip()]
        else:
            seller_descriptions = []

        # Construcția câmpurilor standard
        converted_entry = {
            "id": str(entry.get("ID_Internal", "")),
            "title": entry.get("title", ""),
            "price": entry.get("price", {}).get("value", None),
            "currency": entry.get("price", {}).get("currency", "$"),
            "location": {
                "city": entry.get("city", ""),
                "state": entry.get("state", "")
            },
            "year": entry.get("year", None),
            "make": vehicle.get("full_model", "").split()[0] if vehicle.get("full_model") else None,
            "model": " ".join(vehicle.get("full_model", "").split()[1:]) if vehicle.get("full_model") else None,
            "mileage": int(vehicle.get("odometer", "0").replace(",", "").strip()) if vehicle.get("odometer") else None,
            "transmission": vehicle.get("transmission", "").capitalize() if vehicle.get("transmission") else None,
            "fuel_type": vehicle.get("fuel", "").capitalize() if vehicle.get("fuel") else None,
            "owner_count": None,
            "exterior_color": vehicle.get("paint_color", "").capitalize() if vehicle.get("paint_color") else None,
            "interior_color": None,
            "nhtsa_safety_rating": None,
            "paid_off": "Unknown",
            "vin": vehicle.get("vin", None),
            "seller": {
                "name": None,
                "rating": None,
                "joined_facebook": None,
                "description": {},
            },
            "listed_since": vehicle.get("posted", ""),
            "scraped_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "internal_id": datetime.now().isoformat(),
            "raw_details": {},
            "extra_craig": {}
        }

        # Adăugăm seller_description_X
        for i, desc in enumerate(seller_descriptions):
            key = f"seller_description_{i+1}"
            converted_entry["seller"][key] = desc

        # Concatenăm tot în description
        if seller_descriptions:
            converted_entry["description"] = " ".join(seller_descriptions)
        else:
            converted_entry["description"] = None

        # Adaugă toate câmpurile necunoscute în extra_craig
        for k in entry:
            if k not in ["ID_Internal", "title", "price", "city", "state", "year", "vehicle", "customer_title_description"]:
                extra[k] = entry[k]
        for k in vehicle:
            if k not in ["year", "full_model", "odometer", "fuel", "transmission", "vin", "paint_color", "posted"]:
                extra[k] = vehicle[k]
        if extra:
            converted_entry["extra_craig"] = extra

        converted_list.append(converted_entry)

    return converted_list

def main():
    input_file = "craig_script_json/craiglist_clean_json.json"
    output_file = "craig_script_json/converted_craiglist_with_extras.json"

    # Citește fișierul de intrare
    with open(input_file, "r", encoding="utf-8") as infile:
        craiglist_data = json.load(infile)

    # Conversie
    converted_data = convert_craiglist_to_fb_format(craiglist_data)

    # Scrie fișierul de ieșire
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(converted_data, outfile, indent=2, ensure_ascii=False)

    print(f"[OK] Conversia s-a realizat cu succes in fisierul: {output_file}")

if __name__ == "__main__":
    main()
