import json
import yaml
import os

state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

def generate_yaml_from_dashboard():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    
    json_data_path = os.path.join(current_dir, "data", "craig_form_data.json")
    city_data_path = os.path.join(current_dir, "data", "state_city_clean.json")
    output_yaml = os.path.join(parent_dir, "craigslist.yaml")

    # === Read form data from dashboard ===
    with open(json_data_path, 'r', encoding='utf-8') as f:
        form = json.load(f)

    quick_state = form.get("state", "California")
    purveyor = form.get("purveyor", "owner")
    min_year = form.get("min_year", 2012)
    max_year = form.get("max_year", 2022)
    min_miles = form.get("min_miles", 17000)
    max_miles = form.get("max_miles", 140000)
    max_ads = form.get("max_ads", 9999999)
    search_distance = form.get("search_distance", 25)

    # === Read city list ===
    with open(city_data_path, 'r', encoding='utf-8') as f:
        state_data = json.load(f)

    ordered_states = {quick_state: state_data[quick_state]} if quick_state in state_data else {}
    ordered_states.update({k: v for k, v in state_data.items() if k != quick_state})

    city_list = []
    for state, cities in ordered_states.items():
        abbrev = state_abbreviations.get(state)
        if not abbrev:
            print(f"[!] Missing abbreviation for state: {state}")
            continue
        for city in cities:
            city_list.append(f"{city}, {abbrev}")

    # === Generate YAML ===
    yaml_data = {
        "headless": False,
        "chrome_profile_folder": "chrome_profiles/craigslist",
        "city_list": city_list,
        "search_distance": search_distance,
        "purveyor": purveyor,
        "min_year": min_year,
        "max_year": max_year,
        "min_miles": min_miles,
        "max_miles": max_miles,
        "max_ads": max_ads
    }

    with open(output_yaml, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, sort_keys=False, allow_unicode=True)

    print(f"[✔] craigslist.yaml file generated at: {output_yaml}")

    # === Show first 12 lines and last 7 lines ===
    with open(output_yaml, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("\n[✔] Preview of craigslist.yaml:\n")
    for line in lines[:12]:
        print(line.rstrip())
    
    print("...")  # separator
    
    for line in lines[-7:]:
        print(line.rstrip())

if __name__ == "__main__":
    generate_yaml_from_dashboard()
