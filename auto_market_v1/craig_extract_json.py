import os
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys

import craig_script_json.craig_clean_json as clean_json
sys.stdout.reconfigure(encoding='utf-8')

def extract_price(text):
    match = re.search(r"\$\s*([\d.,]+)", text)
    if match:
        price_str = match.group(1).replace(",", "").strip().split('.')[0]
        try:
            return {"value": int(price_str), "currency": "$"}
        except ValueError:
            return None
    return None

def main():
    BASE_DIR = Path(__file__).resolve().parent
    input_folder = BASE_DIR / "craig_saved_pages"
    output_json_path = BASE_DIR / "craig_script_json" / "craiglist_json.json"
    processed_folder = BASE_DIR / "craig_proccesed_pages"
    processed_folder.mkdir(exist_ok=True)

    existing_data = []
    existing_urls = set()
    if output_json_path.exists():
        with open(output_json_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_urls = {entry["url"] for entry in existing_data}

    entries = existing_data.copy()
    internal_id = len(entries) + 1

    for txt_file in input_folder.glob("*.txt"):
        with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            continue

        data = {"ID_Internal": internal_id}
        data["url"] = lines[0]

        if data["url"] in existing_urls:
            continue

        for i, line in enumerate(lines):
            if line.startswith("TITLE:"):
                data["title"] = line.replace("TITLE:", "").strip()
                title_lower = data["title"].lower()

                if "for sale by owner" in title_lower:
                    data["sale_by"] = "owner"

                loc_match = re.search(r"- ([\w\s]+),\s*([A-Z]{2}) - craigslist", data["title"])
                if loc_match:
                    data["city"] = loc_match.group(1).strip()
                    data["state"] = loc_match.group(2).strip()

                year_match = re.search(r"\b(19|20)\d{2}\b", data["title"])
                if year_match:
                    data["year"] = int(year_match.group(0))

            if line.lower() == "print" and i + 1 < len(lines):
                data["customer_title_description"] = lines[i + 1]

            if "$" in line and "price" not in data:
                price = extract_price(line)
                if price:
                    data["price"] = price

            image_match = re.search(r"image 1 of (\d+)", line.lower())
            if image_match:
                data["images_count"] = int(image_match.group(1))

            if line.startswith("post id:"):
                data["post_id"] = line.replace("post id:", "").strip()

            if line.startswith("posted:"):
                posted_text = line.replace("posted:", "").strip()
                posted_days = re.search(r"(\d+)\s+day", posted_text)
                data["posted_days_ago"] = int(posted_days.group(1)) if posted_days else 1

            if line.startswith("updated:"):
                updated_text = line.replace("updated:", "").strip()
                updated_hours = re.search(r"(\d+)\s+hour", updated_text)
                data["updated_hours_ago"] = int(updated_hours.group(1)) if updated_hours else 1

            if line.lower() == "openstreetmap" and i + 2 < len(lines):
                try:
                    data.setdefault("vehicle", {})["year"] = int(lines[i + 1])
                    data["vehicle"]["full_model"] = lines[i + 2]
                except:
                    pass

            if line.endswith(":") and i + 1 < len(lines):
                key = line[:-1].strip().lower().replace(" ", "_")
                value = lines[i + 1]
                data.setdefault("vehicle", {})[key] = value

            if "qr code link to this post" in line.lower():
                desc_lines = []
                for desc_line in lines[i + 1:]:
                    if desc_line.startswith("post id:"):
                        break
                    desc_lines.append(desc_line)
                data["description"] = " ".join(desc_lines).strip()

        entries.append(data)
        internal_id += 1
        existing_urls.add(data["url"])

        shutil.move(str(txt_file), processed_folder / txt_file.name)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"\n✔️ Procesare completă. {len(entries)} anunțuri salvate în '{output_json_path.relative_to(BASE_DIR)}'.")

    # === Scripturi suplimentare de prelucrare ===
    extra_scripts = [
        "craig_clean_json.py",
        "convert_craigslist_to_standard.py",
        "convert_flags_for_craig.py",
        "cars_tabulator.py",
        "update_tabulator_data.py" 
    ]
    scripts_dir = BASE_DIR / "craig_script_json"

    for script in extra_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"\n▶️ Rulez: {script}...")
            result = subprocess.run(["python", str(script_path)], cwd=BASE_DIR, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[ok] {script} terminat cu succes.")
            else:
                print(f"[EROARE] {script}:\n{result.stderr}")
        else:
            print(f"⚠️ Scriptul {script} nu există în {scripts_dir} (ignorat).")

if __name__ == "__main__":
    main()
