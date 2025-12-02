import os
import json

def fix_chrome_profile(user_data_dir):
    """
    Setează flag-urile din profilul Chrome pentru a evita Restore Pages.
    """
    preferences_path = os.path.join(user_data_dir, 'Default', 'Preferences')
    if os.path.exists(preferences_path):
        try:
            with open(preferences_path, 'r+', encoding='utf-8') as f:
                prefs = json.load(f)
                # Modificăm flag-urile
                prefs['profile']['exit_type'] = 'Normal'
                prefs['profile']['exited_cleanly'] = True
                f.seek(0)
                json.dump(prefs, f, indent=2)
                f.truncate()
            print("✅ Chrome profile fixed: exit_type=Normal, exited_cleanly=True.")
        except Exception as e:
            print(f"⚠️ Eroare la fixarea profilului Chrome: {e}")
    else:
        print(f"⚠️ Preferences file not found at {preferences_path}. Cannot fix profile.")
