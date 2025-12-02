import json
import yaml
import os

def generate_yaml(input_json_path, output_yaml_path, quick_state, price_min, price_max):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ordered_states = {}
    if quick_state in data:
        ordered_states[quick_state] = data[quick_state]

    for state, cities in data.items():
        if state != quick_state:
            ordered_states[state] = cities

    search_tasks = []
    for state, cities in ordered_states.items():
        for city in cities:
            search_tasks.append({
                "city": f"{city}, {state}",
                "price_min": price_min,
                "price_max": price_max
            })

    # Write YAML file
    with open(output_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump({"search_tasks": search_tasks}, f, sort_keys=False, allow_unicode=True)

    print(f"[✔] YAML file generated: {output_yaml_path}")

    # Show first 10 rows exactly as in YAML file
    print("\n[✔] New Config (first 20 YAML lines):\n")
    with open(output_yaml_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            print(line.rstrip())

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

    # Read values from fb_form_data.json
    form_json_path = os.path.join(current_dir, "data", "fb_form_data.json")
    with open(form_json_path, 'r', encoding='utf-8') as f:
        form_data = json.load(f)

    quick_state = form_data.get("quick_state") or form_data.get("state", "California")
    price_min = form_data.get("price_min", 4000)
    price_max = form_data.get("price_max", 14000)

    input_json = os.path.join(current_dir, "data", "state_city_clean.json")
    output_yaml = os.path.join(parent_dir, "facebook.yaml")

    generate_yaml(input_json, output_yaml, quick_state, price_min, price_max)
