import time
from collections import deque
from memory import MemoryManager
from fs import FileSystem
from rich import print


class Kernel:
    """
    The core kernel of the operating system.

    Attributes:
        memory (MemoryManager): The memory management subsystem.
        fs (FileSystem): The file system subsystem.
        scheduler_queue (deque): A queue to manage process scheduling.
    """

    def __init__(self):
        """
        Initialize the Kernel and its subsystems.
        """
        self.memory = MemoryManager()
        self.fs = FileSystem()
        self.scheduler_queue = deque()

    def boot(self):
        """
        Simulates the boot sequence of the operating system.
        """
        print(" [BIOS] Checking Hardware...", end="")
        time.sleep(0.5)
        print(" OK")
        print(" [KERNEL] Initializing Memory...", end="")
        time.sleep(0.5)
        print(" OK")
        print(" [KERNEL] Mounting FileSystem...", end="")
        time.sleep(0.5)
        print(" OK")
        print("\n[bold]--- Welcome to PyOS version 1.0 ---[/bold]\n")

    def run_process(self, name, duration):
        """
        Starts a process and adds it to the scheduler.

        Args:
            name (str): The name of the process.
            duration (str or int): The duration the process should run.
        """
        # 1. Load into RAM
        ram_slot = self.memory.allocate(name, "ACTIVE_DATA")
        if ram_slot is False:
            print(f" [ERROR] Out of Memory! Cannot start {name}.")
            return

        # 2. Add to CPU Schedule
        try:
            duration_int = int(duration)
        except ValueError:
            print(f" [ERROR] Invalid duration for process '{name}'.")
            self.memory.free(name)
            return

        self.scheduler_queue.append({"name": name, "time": duration_int})
        print(f" [KERNEL] Process '{name}' started (PID: {ram_slot})")

        # 3. Run Scheduler (Simplified: runs immediately)
        self._execute_schedule()

    def _execute_schedule(self):
        """
        Executes processes in the scheduler queue using a Round Robin approach.
        """
        print("   >>> [CPU] Starting Execution Loop...")
        while self.scheduler_queue:
            proc = self.scheduler_queue.popleft()
            print(f"   >>> Running {proc['name']}...")
            time.sleep(1)  # Simulate work

            proc["time"] -= 1
            if proc["time"] > 0:
                self.scheduler_queue.append(proc)  # Round Robin
            else:
                print(f"   >>> {proc['name']} Finished.")
                self.memory.free(proc["name"])  # Free RAM
        print("   >>> [CPU] Idle.")

    # --- System Calls (The Bridge) ---
    def sys_write(self, fname, data):
        """
        System call to write data to a file.

        Args:
            fname (str): The filename.
            data (str): The data to write.
        """
        if self.fs.save(fname, data):
            print(f" [IO] Saved '{fname}' successfully.")
        else:
            print(" [IO] Error: Disk Full.")

    def sys_read(self, fname):
        """
        System call to read data from a file.

        Args:
            fname (str): The filename to read.
        """
        data = self.fs.read(fname)
        if data:
            print(f" [IO] READ OUTPUT: {data}")
        else:
            print(f" [IO] Error: File '{fname}' not found.")
