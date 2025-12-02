import subprocess
import os
import sys

def start_program():
    script_path = os.path.abspath('../alfa_facebook.py')
    script_dir = os.path.dirname(script_path)  # The folder where alfa_facebook.py is located

    # ✅ Determine the full path to dashboard_facebook/program_pid.txt
    dashboard_path = os.path.abspath(os.path.dirname(__file__))
    pid_file_path = os.path.join(dashboard_path, "program_pid.txt")

    # Launch cmd.exe in the correct directory and start the script
    proc = subprocess.Popen(
        ["cmd.exe", "/k", sys.executable, script_path],
        cwd=script_dir,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # Save the PID to the correct location
    with open(pid_file_path, 'w') as f:
        f.write(str(proc.pid))

    print(f"✅ The program was launched with PID {proc.pid}.")

if __name__ == "__main__":
    start_program()
