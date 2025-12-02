import subprocess
import os
import sys

def start_generate_yaml_craig():
    script_name = 'craigslist_yaml_generator.py'

    # Folderul unde se află scriptul
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'yaml_generator'))

    if sys.platform == "win32":
        # Comandă pentru Windows (CMD)
        command = (
            f'start cmd /c "cd /d {script_path} && echo === RUNNING craigslist_yaml_generator.py === && '
            f'python {script_name} & timeout /t 8 >nul"'
        )
        subprocess.Popen(command, shell=True)

    else:
        # Comandă pentru Linux (Gnome Terminal)
        subprocess.Popen(
            ['gnome-terminal', '--', 'bash', '-c', f'cd {script_path}; python3 {script_name}; sleep 8'],
            cwd=script_path
        )

if __name__ == "__main__":
    start_generate_yaml_craig()
