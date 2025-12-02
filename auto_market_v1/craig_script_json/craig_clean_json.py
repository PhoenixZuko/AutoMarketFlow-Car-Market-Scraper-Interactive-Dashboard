import json
import re
import shutil
from pathlib import Path

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
    "]+", flags=re.UNICODE
)

def remove_emoji_only(text):
    if isinstance(text, str):
        text_no_emoji = emoji_pattern.sub('', text)
        return re.sub(r'\s+', ' ', text_no_emoji).strip()
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

def main():
    input_file = Path("craig_script_json/craiglist_json.json")  # <- corect input
    output_folder = Path("craig_script_json")
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "craiglist_clean_json.json"  # <- fișier de output
    temp_file = output_folder / "craiglist_clean_temp.json"


    if not input_file.exists():
        return

    with open(input_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    if not data:
        return

    cleaned = clean_text_fields(data)

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    shutil.move(temp_file, output_file)

if __name__ == "__main__":
    main()
