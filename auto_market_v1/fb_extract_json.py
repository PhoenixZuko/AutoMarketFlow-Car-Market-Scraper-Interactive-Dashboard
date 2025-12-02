import os
import json
import shutil
from datetime import datetime
import re
import fb_script_json.clean_emoticone as clean
import fb_script_json.structure_data as structure
import fb_script_json.rating_json as rating
import fb_script_json.calculate_rating_seller as rating_seller
import fb_script_json.positive_flags as  positive_flags
import fb_script_json.tubulator as tubulator
from fb_script_json.tubulator import verifica_si_concateaza_tubulator_display
import tubulator_display.update_tabulator_data as update_tab


def parse_business_details(lines, start_index):
    business_details = {}
    details = {}
    idx = start_index
    detail_counter = 1

    # Continuăm până dăm de "Message seller" sau "Learn more"
    while idx < len(lines):
        line = lines[idx]
        if "Message seller" in line or "Learn more" in line:
            break
        if line.strip():
            details[f"business_detail{detail_counter}"] = line.strip()
            detail_counter += 1
        idx += 1

    if details:
        business_details['details'] = details
    else:
        business_details['details'] = None

    return business_details

def parse_text_to_json(text, file_id):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    data = {}

    # Add ID and Facebook URL
    data['id'] = file_id
    data['facebook_url'] = f"https://www.facebook.com/marketplace/item/{file_id}"

    # === Title ===
    def is_timer_line(line):
        return bool(re.match(r'^\d+:\d+\s*/\s*\d+:\d+$', line))
    
    data['title'] = None
    title_line = None
    for line in lines:
        if not is_timer_line(line) and len(line.split()) >= 2:
            data['title'] = line.strip()
            title_line = line.strip()
            break

    # === Price and Currency ===
    def is_price_line(line):
        return bool(re.match(r'^[^\d\s]{0,3}\d{1,3}(?:,\d{3})*(?:\.\d{2})?$|^[^\d\s]{0,3}\d+$', line.strip()))
    
    data['price'] = None
    data['currency'] = None
    
    for line in lines:
        if line.strip() == title_line:
            continue  # Skip title
        if is_price_line(line):
            raw_line = line.strip()
            currency_match = re.match(r'^([^\d\s]{1,3})', raw_line)
            if currency_match:
                currency = currency_match.group(1)
                data['currency'] = currency
            else:
                data['currency'] = None

            price_clean = re.sub(r'^[^\d\s]+', '', raw_line)
            price_clean = price_clean.replace(',', '').strip()

            try:
                if '.' in price_clean:
                    data['price'] = float(price_clean)
                else:
                    data['price'] = int(price_clean)
            except ValueError:
                data['price'] = price_clean  # fallback
    
            break

    # === Listed Since ===
    listed_index = lines.index('Listed') if 'Listed' in lines else None
    data['listed_since'] = lines[listed_index + 1] if listed_index is not None and listed_index + 1 < len(lines) else None

    # === Location ===
    location_line = None
    
    # Încearcă să extragi locația din linii cu "in City, ST"
    for line in lines:
        match = re.search(r'in ([A-Za-z\s]+),\s*([A-Z]{2})', line)
        if match:
            city, state = match.group(1).strip(), match.group(2).strip()
            data['location'] = {'city': city, 'state': state}
            break
    else:
        # Fallback: caută linie care pare a fi direct "City, ST"
        for line in lines:
            if re.match(r'^[A-Za-z\s]+,\s*[A-Z]{2}$', line.strip()):
                parts = line.strip().split(',')
                if len(parts) == 2:
                    city = parts[0].strip()
                    state = parts[1].strip()
                    data['location'] = {'city': city, 'state': state}
                    break
        else:
            data['location'] = {'city': None, 'state': None}
    
    # === Vehicle Details ===
    vehicle_details = {}
    details = {}
    try:
        about_index = lines.index('About this vehicle')
        for idx in range(about_index + 1, len(lines)):
            if lines[idx] in ["Seller's description", "Location is approximate", "Seller information"]:
                break
            details[f"id_detail{idx - about_index}"] = lines[idx]
    except:
        pass

    vehicle_details['details'] = details
    data['vehicle_details'] = vehicle_details

    # === Seller's Description ===
    seller_description = {}
    if "Seller's description" in lines:
        seller_index = lines.index("Seller's description") + 1
        desc_lines = []
        while seller_index < len(lines) and "Location is approximate" not in lines[seller_index] and "Seller information" not in lines[seller_index]:
            desc_lines.append(lines[seller_index])
            seller_index += 1
        for idx, line in enumerate(desc_lines, 1):
            if line.strip():
                seller_description[f"id_description{idx}"] = line.strip()
    data['seller_description'] = seller_description

    # === Seller Information ===
    seller_info = {}
    try:
        seller_info_index = lines.index('Seller information') + 1

        while seller_info_index < len(lines):
            potential_name = lines[seller_info_index]
            if potential_name != 'Seller details':
                seller_info['name'] = potential_name
                break
            seller_info_index += 1

        rating_line = lines[seller_info_index + 1]
        if '(' in rating_line and ')' in rating_line:
            rating_number = int(rating_line.replace('(', '').replace(')', '').strip())
            seller_info['rating'] = rating_number
        else:
            seller_info['rating'] = None

        for i in range(seller_info_index, len(lines)):
            if 'Joined Facebook in' in lines[i]:
                seller_info['joined_facebook'] = lines[i].split('Joined Facebook in')[-1].strip()
                break
        else:
            seller_info['joined_facebook'] = None
    except:
        seller_info['name'] = None
        seller_info['rating'] = None
        seller_info['joined_facebook'] = None

    data['seller_information'] = seller_info

    # === Business Details ===
    business_details = {"details": None}
    try:
        if "Business Details" in lines:
            business_index = lines.index("Business Details") + 1
            business_details = parse_business_details(lines, business_index)
    except:
        pass

    data['business_details'] = business_details

   # === Scraped Date & Internal ID ===
    now = datetime.now()
    data['scraped_date'] = now.strftime('%Y-%m-%d %H:%M')
    data['internal_id'] = now.isoformat(timespec='microseconds')  # ex: 2025-06-11T14:59:18.123456

    return data

def process_txt_folder_to_single_json(input_folder, output_file, processed_folder):
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = []

    existing_ids = set(entry['id'] for entry in all_data)

    new_entries = []
    added_count = 0

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            txt_path = os.path.join(input_folder, filename)
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()

            file_id = os.path.splitext(filename)[0]
            if file_id not in existing_ids:
                parsed_data = parse_text_to_json(text, file_id)
                new_entries.append(parsed_data)
                added_count += 1

                shutil.move(txt_path, os.path.join(processed_folder, filename))

    all_data.extend(new_entries)
        # ✅ Adaugă internal_id și scraped_date pentru intrările vechi (fără ele)
    for entry in all_data:
        if 'internal_id' not in entry:
            now = datetime.now()
            entry['internal_id'] = now.isoformat(timespec='microseconds')
            print(f"[Upgrade] Added missing internal_id for ID {entry.get('id')}")

        if 'scraped_date' not in entry:
            now = datetime.now()
            entry['scraped_date'] = now.strftime('%Y-%m-%d %H:%M')
            print(f"[Upgrade] Added missing scraped_date for ID {entry.get('id')}")


    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    print(f"✅ Added {added_count} new listings. Total now: {len(all_data)} listings.")

def main():
    print("🔍 Începem extracția și procesarea inițială...")

    input_folder = "saved_pages"
    output_file = os.path.join("fb_script_json", "all_data.json")
    processed_folder = "processed_pages"

    process_txt_folder_to_single_json(input_folder, output_file, processed_folder)

    print("🚀 Running clean_emoticone.py...")
    clean.main()

    print("🚀 Running structure_data.py...")
    structure.main()

    print("🚀 Running rating_json.py...")
    rating.main()
    
    print("🎯 Running rating_seller.py...")
    rating_seller.main()  # apoi adaugă seller_score + total_score

    print("🎯 Running positive_flags.py...")
    positive_flags.main() 

    print("🎯 Running tubulator.py...")
    tubulator.main() 

    verifica_si_concateaza_tubulator_display()

    print("📊 Running update_tabulator_data.py...")
    update_tab.convert_tabulator_data("tubulator_display/cars_tabulator.json")

if __name__ == "__main__":
    main()