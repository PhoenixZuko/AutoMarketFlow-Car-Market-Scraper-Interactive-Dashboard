import json
import yaml
from datetime import datetime
import os


def is_classic(year):
    return datetime.now().year - year >= 30

# Funcție care returnează categoria finală
def categorize_score(score, year):
    year = year or 1900  # fallback dacă year este None sau 0
    if is_classic(year):
        return "Classic"
    elif score >= 25:
        return "Excellent"
    elif score >= 18:
        return "Very Good"
    elif score >= 12:
        return "Good"
    elif score >= 6:
        return "Weak"
    else:
        return "Very Weak"
    if not car.get('year'):
     print(f"Car with ID {car.get('id')} is missing 'year'")
     
# Load config YAML


def load_config(yaml_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))  # ← folderul în care e scriptul
    yaml_path = os.path.join(current_dir, yaml_file)          # ← caută lângă script
    print(f"🔍 Caut config.yaml la: {yaml_path}")
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"❌ Fișierul config.yaml nu a fost găsit la: {yaml_path}")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Load cars JSON
def load_cars(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:   # 🔥 Adăugat encoding='utf-8'
        return json.load(f)


# Save updated cars
def save_cars(cars, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cars, f, indent=2, ensure_ascii=False)

# Load existing output to detect changes
def load_existing_output(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return {car['id']: car for car in json.load(f)}
    return {}

# Detect car type
def detect_type_car(car, type_mapping):
    title = (car.get('title') or '').lower()
    model = (car.get('model') or '').lower()
    text = f"{title} {model}"

    # 🥇 Prioritizează Wagon dacă apare în text
    if 'wagon' in text:
        return 'Wagon'

    # 🧠 Continuă cu regulile din YAML
    for car_type, details in type_mapping.items():
        for keyword in details['keywords']:
            if keyword.lower() in text:
                return car_type

    return 'Unknown'



# Calculate score for one car
from datetime import datetime

def calculate_car_score(car, config):
    score = 0
    rules = config['scoring_rules_car']

    year = int(car.get('year') or 0)
    mileage = int(car.get('mileage') or 0)
    price = int(car.get('price') or 0)
    vin = str(car.get('vin') or '')
    nhtsa_rating = int(car.get('nhtsa_safety_rating') or 0)
    title_status = (car.get('title_status') or '').lower()
    owner_count = int(car.get('owner_count') or 3)
    description = car.get('description') or ''
    listed_date = car.get('listed_date') or ''
    transmission = (car.get('transmission') or '').lower()
    fuel_type = (car.get('fuel_type') or '').lower()
    make = (car.get('make') or '')
    raw_details = car.get('raw_details', {})
    paid_off = car.get('paid_off')
    
    # Year
    try:
        score += eval(rules['year']['formula'])
    except Exception as e:
        print(f"Year error: {e}")

    # Mileage
    try:
        score += eval(rules['mileage']['formula'])
    except Exception as e:
        print(f"Mileage error: {e}")

    # Price
    try:
        if price <= rules['price']['max_price']:
            score += eval(rules['price']['formula'])
    except Exception as e:
        print(f"Price error: {e}")

    # Owner Count
    if owner_count == 1:
        score += rules['owner_count']['one_owner_bonus']
    elif owner_count == 2:
        score += rules['owner_count']['two_owners_bonus']
    else:
        score += rules['owner_count']['more_owners_penalty']

    # Title Status
    if 'clean' in title_status:
        score += rules['title_status']['clean_title_bonus']
    elif 'rebuilt' in title_status:
        score += rules['title_status']['rebuilt_title_penalty']

    # VIN
    if vin.strip():
        score += rules['vin']['vin_present_bonus']

    # NHTSA Safety Rating
    try:
        score += eval(rules['nhtsa_safety_rating']['formula'])
    except Exception as e:
        print(f"NHTSA error: {e}")

    # Description Lines
    desc_lines = description.count('\n') + 1
    min_lines = rules['description_analysis']['min_lines']
    if desc_lines > min_lines:
        score += (desc_lines - min_lines) * rules['description_analysis']['bonus_per_extra_line']

    # Keywords in Description
    for keyword in rules['description_keywords']['keywords']:
        if keyword['word'].lower() in description.lower():
            score += keyword['points']

    # Listing Age
    if listed_date:
        try:
            listed_date_obj = datetime.strptime(listed_date, '%Y-%m-%d')
            days_old = (datetime.now() - listed_date_obj).days
            for penalty in rules['listing_age']['penalties']:
                if days_old > penalty['days']:
                    score += penalty['points']
        except Exception as e:
            print(f"Date error: {e}")

    # --- New Additions ---

    # Popular Brand Bonus
    if make in rules['popular_brand']['brands']:
        score += rules['popular_brand']['bonus']

    # Transmission Type Bonus/Penalty
    if 'automatic' in transmission:
        score += rules['transmission_type']['automatic_bonus']
    elif 'manual' in transmission:
        score += rules['transmission_type']['manual_penalty']

    # Fuel Type Bonus/Penalty
    if 'electric' in fuel_type:
        score += rules['fuel_type']['electric_bonus']
    elif 'diesel' in fuel_type:
        score += rules['fuel_type']['diesel_penalty']

    # Car Condition Bonus/Penalty
    condition = raw_details.get('vehicle_details_1', '').lower()
    if 'excellent' in condition:
        score += rules['condition']['excellent_bonus']
    elif 'fair' in condition:
        score += rules['condition']['fair_bonus']
    elif 'poor' in condition:
        score += rules['condition']['poor_penalty']

    # Paid Off Bonus/Penalty
    if paid_off == True:
        score += rules['paid_off']['paid_off_bonus']
    elif paid_off == False:
        score += rules['paid_off']['not_paid_penalty']

    # No Damage Bonus
    damage_info = raw_details.get('vehicle_details_3', '').lower()
    if 'no significant damage' in damage_info:
        score += rules['no_damage']['no_damage_bonus']

    return round(score, 2)






# Generate conclusion based on score using config
def generate_conclusion(score, config):
    conclusion_rules = config.get('conclusion_rules', [])
    for rule in conclusion_rules:
        if score >= rule['min_score']:
            return rule['label']
    return "Unknown"


# Main Program
def main():
    config = load_config('config.yaml')
    cars = load_cars('fb_structure.json')

    output_path = os.path.join(os.getcwd(), "fb_rating_json.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    existing_cars = load_existing_output(output_path)

    updated_cars = []

    for car in cars:
        car_id = car.get('id')
        existing = existing_cars.get(car_id)

        type_car = detect_type_car(car, config['type_car_mapping'])
        car_score = calculate_car_score(car, config)
        
        has_changes = (
            not existing or
            existing.get('type_car') != type_car or
            existing.get('car_score') != car_score
        )
        
        if has_changes:
            car['type_car'] = type_car
            car['car_score'] = car_score
            # Eliminăm total_score și conclusion
            car.pop('total_score', None)
            car.pop('conclusion', None)
            updated_cars.append(car)
        else:
            updated_cars.append(existing)
        

    save_cars(updated_cars, output_path)

    for car in updated_cars:
        print(f"ID: {car.get('id')} | Type: {car['type_car']} | Car Score: {car['car_score']}")


    print(f"✅ Final file saved at: {output_path}")


if __name__ == "__main__":
    main()