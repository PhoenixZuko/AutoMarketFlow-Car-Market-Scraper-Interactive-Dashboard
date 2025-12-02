import subprocess
import os
import sys

def start_extract_json():
    # Numele scriptului
    script_name = 'craig_extract_json.py'
    # Directorul proiectului
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    if sys.platform == "win32":
        # Adaugam echo %CD% ca sa vezi folderul curent
        command = f'cmd /c "echo Current Directory: %CD% && echo Running: python {script_name} && python {script_name} & timeout /t 5"'
        subprocess.Popen(
            f'start {command}',
            cwd=project_dir,   # <<< FOARTE IMPORTANT asta seteaza folderul de lucru
            shell=True
        )
    else:
        subprocess.Popen(
            ['gnome-terminal', '--', 'bash', '-c', f'pwd; python3 {script_name}; sleep 5'],
            cwd=project_dir
        )

if __name__ == "__main__":
    start_extract_json()
