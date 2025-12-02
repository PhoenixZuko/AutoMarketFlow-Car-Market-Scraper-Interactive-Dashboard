import os
import psutil

def stop_program():
    pid_file = 'program_pid.txt'

    if not os.path.exists(pid_file):
        print("⚠️ The file program_pid.txt does not exist!")
        return

    with open(pid_file, 'r') as f:
        pid = int(f.read().strip())

    if not psutil.pid_exists(pid):
        print(f"⚠️ Process with PID {pid} no longer exists!")
        return

    try:
        print(f"🛑 Terminating process with PID {pid} and all its children...")
        parent = psutil.Process(pid)

        # 💥 Get the child processes once
        children = parent.children(recursive=True)

        # Terminate child processes first
        for child in children:
            print(f"   🛑 Terminating child PID {child.pid}...")
            child.terminate()

        # Wait for all children to terminate
        gone, still_alive = psutil.wait_procs(children, timeout=5)

        # Terminate the parent process
        parent.terminate()
        parent.wait(timeout=5)

        # 🧹 Optionally delete the PID file
        os.remove(pid_file)

        print("✅ The process and all children have been successfully terminated.")
    except Exception as e:
        print(f"⚠️ Error while terminating process: {e}")

if __name__ == "__main__":
    stop_program()
