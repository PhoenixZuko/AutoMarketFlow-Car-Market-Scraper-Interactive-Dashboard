import json
import re

def main():
    keyword_aliases = {
        "clean title": ["clean tittle", "cleen title", "clear title"],
        "no issues": ["no issue", "no isues", "no problems"],
        "reliable": ["relible", "reliabel", "relaiable"],
        "accident": ["acident", "aciddent"],
        "salvage": ["salvadge", "salvge", "salvej"],
        "broken": ["brokken"],
        "well maintained": ["well maintained", "maintained well"],
        "garage kept": ["garage kept", "kept in garage"],
        "new tires": ["brand new tires", "new tire"],
        "service records": ["full service records", "maintenance history"],
        "damage": ["damaged", "demage"],
        "low miles": ["low mileage", "few miles", "under mileage"],
        "runs great": ["runs perfect", "drives great", "drives well"],
        "new brakes": ["brand new brakes"],
        "non smoker": ["non-smoker", "never smoked"],
        "regular maintenance": ["regularly maintained", "maintenance up to date"],
        "smog passed": ["passed smog", "smog check done"],
        "recently serviced": ["recently checked", "just serviced"],
        "good tires": ["tires in good shape"],
        "cold ac": ["ice cold ac", "ac works great"]
    }

    positive_main = [
        "joined early", "detailed info", "clean title", "well maintained",
        "reliable", "no issues", "garage kept", "new tires",
        "service records", "good condition", "low miles", "runs great",
        "new brakes", "non smoker", "regular maintenance", "smog passed",
        "recently serviced", "good tires", "cold ac"
    ]

    negative_main = ["no title", "parts only", "accident", "damage", "bad condition",
                     "salvage", "broken", "poor description"]

    positive_keywords = set()
    negative_keywords = set()
    for k in positive_main:
        positive_keywords.add(k)
        positive_keywords.update(keyword_aliases.get(k, []))
    for k in negative_main:
        negative_keywords.add(k)
        negative_keywords.update(keyword_aliases.get(k, []))

    reverse_alias_map = {}
    for main, aliases in keyword_aliases.items():
        for alias in aliases:
            reverse_alias_map[alias] = main

    def normalize_keywords(keyword_list):
        normalized = set()
        for word in keyword_list:
            normalized.add(reverse_alias_map.get(word, word))
        return sorted(normalized)

    with open("fb_cars_rating_seller.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    positive_count = 0
    negative_count = 0

    for car in cars:
        text_sources = []

        seller = car.get("seller", {})
        for i in range(1, 30):
            val = seller.get(f"seller_description_{i}")
            if val and isinstance(val, str):
                text_sources.append(val)

        all_text = " ".join(text_sources).lower()
        all_text = re.sub(r"[^\w\s]", " ", all_text)
        all_text = re.sub(r"\s+", " ", all_text).strip()

        positives = []
        negatives = []

        for word in positive_keywords:
            if word in all_text:
                positives.append(word)

        for word in negative_keywords:
            is_negated = any(
                re.search(rf"\bno {word}\b", all_text) or
                re.search(rf"\bno {word}s\b", all_text) or
                re.search(rf"\bno {word}es\b", all_text)
                for word in [word.rstrip('s')]
            )
            if not is_negated and word in all_text:
                negatives.append(word)

        positives = normalize_keywords(positives)
        negatives = normalize_keywords(negatives)

        car["positive_flags"] = f"{len(positives)} | {', '.join(positives)}" if positives else "0 |"
        car["negative_flags"] = f"{len(negatives)} | {', '.join(negatives)}" if negatives else "0 |"
        car["positive_flags_list"] = positives
        car["negative_flags_list"] = negatives
        car["has_clean_title"] = 1 if "clean title" in positives else 0
        vin = car.get("vin")
        car["has_vin"] = 1 if isinstance(vin, str) and len(vin.strip()) >= 10 else 0

        if "seller" in car and car["seller"].get("rating") is None:
            car["seller"]["rating"] = 0

        car["car_score"] = int(car.get("car_score", 0))
        car["seller_score"] = int(car.get("seller_score", 0))
        car.setdefault("type_car", "unknown")

        if positives:
            positive_count += 1
        if negatives:
            negative_count += 1

    with open("fb_cars_with_flags_final.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=2, ensure_ascii=False)

    print(f"✅ Total cars processed: {len(cars)}")
    print(f"🟢 Cars with positive flags: {positive_count}")
    print(f"🔴 Cars with negative flags: {negative_count}")
    print("📁 File saved: fb_cars_with_flags_final.json")
    

if __name__ == "__main__":
    main()
