import json
import yaml
import os
import re
from datetime import datetime, timedelta


def clean_vehicle_details(car):
    details = car.get("raw_details", {})
    keywords_to_avoid = [
        "MPG", "MPG city", "highway", "combined",
        "Safety rating", "title", "damage", "problems", "Money is still owed"
    ]
    new_details = {}
    for key, value in details.items():
        if not any(keyword.lower() in value.lower() for keyword in keywords_to_avoid):
            new_details[key] = value
    car["raw_details"] = new_details


def save_clean_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_yaml_config(path='config_seller.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def calculate_seller_score(seller, config):
    year_now = config.get('year_now', datetime.now().year)
    rules = config['seller_score_rules']

    rating = seller.get('rating')
    joined = seller.get('joined_facebook')

    if rating is None:
        if joined is not None and str(joined).isdigit():
            if int(joined) == year_now:
                return rules['no_rating']['current_year_penalty']
            else:
                return rules['no_rating']['past_year_bonus']
        else:
            return 0
    else:
        try:
            return rules['rated_user']['penalty_per_rating_point'] * int(rating)
        except (ValueError, TypeError):
            return 0


def convert_listed_since_to_hours_string(listed_since, scraped_date):
    if not listed_since:
        return listed_since

    listed_since = listed_since.lower().strip()
    scraped_dt = datetime.strptime(scraped_date, "%Y-%m-%d %H:%M")

    delta = None

    if re.match(r"\d+\s+year", listed_since):
        years = int(re.findall(r"\d+", listed_since)[0])
        delta = timedelta(days=years * 365)
    elif re.match(r"\d+\s+week", listed_since):
        weeks = int(re.findall(r"\d+", listed_since)[0])
        delta = timedelta(weeks=weeks)
    elif re.match(r"\d+\s+day", listed_since):
        days = int(re.findall(r"\d+", listed_since)[0])
        delta = timedelta(days=days)
    elif re.match(r"\d+\s+hour", listed_since):
        hours = int(re.findall(r"\d+", listed_since)[0])
        delta = timedelta(hours=hours)
    elif re.match(r"\d+\s+minute", listed_since):
        minutes = int(re.findall(r"\d+", listed_since)[0])
        delta = timedelta(minutes=minutes)
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

    return f"{hours_since_posted}"


def analyze_descriptions_for_flags(car, config):
    text_sources = []

    if isinstance(car.get("description"), str):
        text_sources.append(car.get("description"))
    if isinstance(car.get("raw_details"), dict):
        text_sources.extend(car.get("raw_details").values())

    for i in range(1, 30):
        key = f"seller_description_{i}"
        val = car.get(key)
        if val and isinstance(val, str):
            text_sources.append(val)

    all_text = " ".join(text_sources).lower()

    positives = []
    negatives = []

    for word in config.get("positive_keywords", []):
        if word in all_text:
            positives.append(word)

    for word in config.get("negative_keywords", []):
        if word in all_text:
            negatives.append(word)

    car["positive_flags"] = f"{len(positives)} | {', '.join(positives)}" if positives else "0 |"
    car["negative_flags"] = f"{len(negatives)} | {', '.join(negatives)}" if negatives else "0 |"


def process_cars(data, config):
    for car in data:
        clean_vehicle_details(car)
        analyze_descriptions_for_flags(car, config)
        seller = car.get('seller', {})
        seller_score = calculate_seller_score(seller, config)
        car['seller_score'] = seller_score
        car_score = car.get('car_score', 0)
        total_score = round(car_score + seller_score, 2)
        car['total_score'] = total_score

        listed_since = car.get("listed_since")
        scraped_date = car.get("scraped_date")
        if listed_since and scraped_date:
            car["listed_since"] = convert_listed_since_to_hours_string(listed_since, scraped_date)

        if 'conclusion' in car:
            del car['conclusion']

    return data


def round_floats_in_dict(data):
    if isinstance(data, dict):
        return {
            key: round_floats_in_dict(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [round_floats_in_dict(item) for item in data]
    elif isinstance(data, float):
        return int(round(data)) if data.is_integer() else round(data)
    elif isinstance(data, str):
        try:
            num = float(data)
            return int(round(num)) if num.is_integer() else round(num)
        except ValueError:
            return data
    else:
        return data


def main():
    config = load_yaml_config('config_seller.yaml')
    cars = load_json('fb_rating_json.json')
    updated_cars = process_cars(cars, config)
    cleaned_output = round_floats_in_dict(updated_cars)

    output_path = os.path.join("fb_cars_rating_seller.json")
    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    save_json(output_path, cleaned_output)
    print(f"✔ Fișier final salvat în: {os.path.abspath(output_path)}")


if __name__ == '__main__':
    main()
