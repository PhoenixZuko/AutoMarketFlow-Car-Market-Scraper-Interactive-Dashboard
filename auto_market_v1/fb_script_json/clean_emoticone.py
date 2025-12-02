import json
import re
import shutil

# Regex-ul și funcțiile LE LĂSĂM AFARĂ ca să fie globale
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002500-\U00002BEF"
    "\u200d"
    "\u2640-\u2642"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "\uFE0F"
    "]+",
    flags=re.UNICODE
)

def remove_emoji_only(text):
    if isinstance(text, str):
        text_no_emoji = emoji_pattern.sub('', text)
        text_clean = re.sub(r'\s+', ' ', text_no_emoji).strip()
        return text_clean
    return text

def clean_text_fields(data):
    if isinstance(data, dict):
        return {k: clean_text_fields(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_text_fields(item) for item in data]
    elif isinstance(data, str):
        return remove_emoji_only(data)
    else:
        return data

# 🔥 TOT codul tău de lucru îl punem ÎN funcția main()
def main():
    # PAS 1: Citește fișierul original
    with open('fb_script_json/all_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # PAS 2: Curăță toate textele
    cleaned_data = clean_text_fields(data)

    # PAS 3: Salvează în temp_clean.json
    temp_filename = 'temp_clean.json'
    with open(temp_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Curățare GENERALĂ emoji completă — salvat temporar în {temp_filename}.")

    # PAS 4: Înlocuiește originalul all_data.json cu temp_clean.json
    shutil.move(temp_filename, 'fb_script_json/all_data.json')

    print(f"✅ Succes! Fișierul all_data.json a fost înlocuit cu varianta curată fără emoji.")

# Standard entry point
if __name__ == "__main__":
    main()
