import os
import json

def convert_tabulator_data(input_file_path="tubulator_display/cars_tabulator.json"):
    output_dir = os.path.join("..", "display", "data")
    os.makedirs(output_dir, exist_ok=True)

    intermediate_file = os.path.join(output_dir, "cars_tabulator_temp.json")
    final_output_file = os.path.join(output_dir, "cars_tabulator.json")

    all_data = []
    existing_urls = set()
    next_id = 1

    # 1. Citim datele existente (daca exista)
    if os.path.exists(final_output_file):
        try:
            with open(final_output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for item in existing_data:
                    if isinstance(item, dict):
                        url = item.get("url")
                        if url:
                            existing_urls.add(url)
                        item["new"] = 0
                        all_data.append(item)
                existing_ids = [item.get("id", 0) for item in existing_data if isinstance(item, dict)]
                next_id = max(existing_ids) + 1 if existing_ids else 1
        except Exception as e:
            print(f"[EROARE] Nu pot citi {final_output_file}: {e}")

    # 2. Citim fisierul de intrare
    if not os.path.exists(input_file_path):
        print(f"[EROARE] Fisierul de intrare nu exista: {input_file_path}")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            with open(intermediate_file, 'w', encoding='utf-8') as out_f:
                json.dump(new_data, out_f, indent=2, ensure_ascii=False)
            print(f"[INFO] Fisier intermediar salvat: {intermediate_file}")
    except Exception as e:
        print(f"[EROARE] Nu pot citi fisierul de intrare: {e}")
        return

    # 3. Parcurgem toate fisierele JSON din folder, mai putin fisierul final
    try:
        for filename in os.listdir(output_dir):
            if filename.endswith(".json") and filename != "cars_tabulator.json":
                file_path = os.path.join(output_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        if isinstance(content, list):
                            for entry in content:
                                if isinstance(entry, dict):
                                    url = entry.get("url")
                                    if url and url not in existing_urls:
                                        entry["id"] = next_id
                                        entry["new"] = 1
                                        all_data.append(entry)
                                        existing_urls.add(url)
                                        next_id += 1
                        else:
                            print(f"[AVERTISMENT] {filename} nu contine o lista valida.")
                except Exception as e:
                    print(f"[EROARE] Nu pot procesa {filename}: {e}")
    except Exception as e:
        print(f"[EROARE] Eroare la parcurgerea folderului: {e}")
        return

    # 4. Scriem toate datele combinate in fisierul final
    try:
        with open(final_output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Salvare completa in {final_output_file} — total: {len(all_data)} intrari.")
    except Exception as e:
        print(f"[EROARE] Nu pot salva fisierul final: {e}")

# Pentru rulare directa
if __name__ == "__main__":
    convert_tabulator_data("tubulator_display/cars_tabulator.json")
