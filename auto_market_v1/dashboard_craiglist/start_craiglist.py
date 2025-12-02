import subprocess
import os
import sys

def start_program():
    script_path = os.path.abspath('../alfa_craigslist.py')
    script_dir = os.path.dirname(script_path)  # <<< Folderul unde e scriptul

    # Open cmd.exe in the correct working directory
    proc = subprocess.Popen(
        ["cmd.exe", "/k", sys.executable, script_path],
        cwd=script_dir,  # <<< set correct working directory
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    with open('craiglist_pid.txt', 'w') as f:
        f.write(str(proc.pid))

    print(f"✅ Craigslist program started with PID {proc.pid}.")

if __name__ == "__main__":
    start_program()
