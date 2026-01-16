import time
from collections import deque


class Kernel:
    def __init__(self):
        self.process_queue = deque()

    def add_process(self, name, duration):
        """
        Adds a fake process/app to our OS
            args:
                name: str, duration: any
        """
        self.process_queue.append({"name": name, "time_left": duration})
        print(f"[KERNEL] Process added {name} needs {duration}s time to complete.")

    def run(self):
        """Runs the Kernel"""
        print("\n[KERNEL] Starting Scheduler (Round Robin mode...)")
        print("_" * 40)
        # Keeps looping until no processes are left
        while self.process_queue:
            current_process = self.process_queue.popleft()
            print(f"    >>> CPU is running {current_process['name']}")
            time.sleep(1)
            current_process["time_left"] -= 1
            if current_process["time_left"] > 0:
                # If not finished, save it and put it back at the end of the line
                print(
                    f"       [Interrupt] Time slice over! {current_process['name']} saved."
                )
                self.process_queue.append(current_process)
            else:
                # If finished, close it
                print(f"       [Success] {current_process['name']} finished execution!")
        print("-" * 40)
        print("[KERNEL] All processes finished! System idle.")


# --- User Land (Simulation) ---

# Initialize OS
my_os = Kernel()

# Launch Apps
my_os.add_process("Spotify.exe", 3)  # Needs 3 seconds
my_os.add_process("Chrome.exe", 2)  # Needs 2 seconds
my_os.add_process("VsCode.exe", 4)  # Needs 4 seconds

# Start the OS
my_os.run()
