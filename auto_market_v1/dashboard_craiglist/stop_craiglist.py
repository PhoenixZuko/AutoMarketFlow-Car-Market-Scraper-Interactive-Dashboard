import os
import psutil

def stop_program():
    pid_file = 'craiglist_pid.txt'

    if not os.path.exists(pid_file):
        print("⚠️ PID file craiglist_pid.txt does not exist!")
        return

    with open(pid_file, 'r') as f:
        pid = int(f.read().strip())

    if not psutil.pid_exists(pid):
        print(f"⚠️ No process found with PID {pid}.")
        return

    try:
        print(f"🛑 Terminating Craigslist process PID {pid} and all its children...")
        parent = psutil.Process(pid)

        children = parent.children(recursive=True)
        for child in children:
            print(f"   🛑 Terminating child PID {child.pid}...")
            child.terminate()

        # Wait for children to terminate
        gone, still_alive = psutil.wait_procs(children, timeout=5)

        # Terminate the parent process
        parent.terminate()
        parent.wait(timeout=5)

        # Clean up PID file
        os.remove(pid_file)

        print(f"✅ Craigslist process and all child processes have been terminated.")
    except Exception as e:
        print(f"⚠️ Error during termination: {e}")

if __name__ == "__main__":
    stop_program()
