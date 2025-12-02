import json
import re
import os

def main():
    try:
        with open('fb_cars_with_flags_final.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Input file 'fb_cars_with_flags_final.json' not found.")
        return

    output = []
    for item in data:
        try:
            title = item.get("title", "")
            if not isinstance(title, str):
                title = ""
            title = re.sub(r"^\d{4}\s+", "", title)

            new_entry = {
                "id": item.get("id"),
                "title": title,
                "price": f'{item.get("price", "")} $',
                "year": item.get("year"),
                "Brand": item.get("make"),
                "mileage": item.get("mileage"),
                "fuel": (item.get("fuel_type") or "")[:3],
                "Tra": (item.get("transmission") or "")[:3],
                "type": item.get("type_car"),
                "seller": item.get("seller", {}).get("name"),
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
                "since": item.get("listed_since"),
                "score": item.get("car_score"),
                "pflags": item.get("positive_flags"),
                "nflags": item.get("negative_flags"),
                "sscore": item.get("seller_score"),
                "clean": item.get("has_clean_title"),
                "has_vin": item.get("has_vin"),
                "url": f"https://www.facebook.com/marketplace/item/{item.get('id')}"
            }
            output.append(new_entry)
        except Exception as e:
            print(f"Error processing an entry: {e}")

    output_dir = os.path.join(".", "tubulator_display")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cars_tabulator_fb.json")

    try:
        with open(output_path, 'w', encoding='utf-8') as out_f:
            json.dump(output, out_f, indent=2, ensure_ascii=False)
        print(f"✅ Export completed: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"❌ Failed to write output file: {e}")
        return

    # Cleanup
    cleanup_files = [
        "fb_cars_rating_seller.json",
        "fb_cars_with_flags_final.json",
        "fb_rating_json.json",
        "fb_structure.json"
    ]
    for file in cleanup_files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️ Deleted: {file}")
        except Exception as e:
            print(f"⚠️ Could not delete {file}: {e}")


def verifica_si_concateaza_tubulator_display():
    folder = "tubulator_display"
    fb_path = os.path.join(folder, "cars_tabulator_fb.json")
    craig_path = os.path.join(folder, "cars_tabulator_craig.json")
    final_path = os.path.join(folder, "cars_tabulator.json")

    combined_data = []

    # Încarcă datele noi din Facebook
    if os.path.exists(fb_path):
        try:
            with open(fb_path, 'r', encoding='utf-8') as f:
                fb_data = json.load(f)
                if isinstance(fb_data, list):
                    combined_data.extend(fb_data)
                    print(f"✅ {len(fb_data)} intrări din Facebook adăugate.")
                else:
                    print(f"⚠️ {fb_path} nu conține o listă.")
        except Exception as e:
            print(f"❌ Eroare la citirea {fb_path}: {e}")
    else:
        print(f"❌ {fb_path} nu există. Nu s-au găsit date Facebook.")
        return  # Ieși dacă nu există fișierul principal

    # Dacă există și Craig, adaugă și acele date
    if os.path.exists(craig_path):
        try:
            with open(craig_path, 'r', encoding='utf-8') as f:
                craig_data = json.load(f)
                if isinstance(craig_data, list):
                    combined_data.extend(craig_data)
                    print(f"➕ {len(craig_data)} intrări din Craig adăugate.")
                else:
                    print(f"⚠️ {craig_path} nu conține o listă.")
        except Exception as e:
            print(f"❌ Eroare la citirea {craig_path}: {e}")
    else:
        print("ℹ️ Craig nu există. Se va salva doar conținutul Facebook.")

    # Salvează rezultatul combinat
    try:
        with open(final_path, 'w', encoding='utf-8') as out_f:
            json.dump(combined_data, out_f, indent=2, ensure_ascii=False)
        print(f"💾 Scris cu succes: {final_path} ({len(combined_data)} intrări)")
    except Exception as e:
        print(f"❌ Eroare la scrierea fișierului final: {e}")


if __name__ == "__main__":
    main()
    verifica_si_concateaza_tubulator_display()
