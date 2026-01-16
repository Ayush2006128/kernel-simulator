import time
from collections import deque


# ===================== #
# 1. HARDWARE SIMULATOR #
# ===================== #
class MemoryManager:
    def __init__(self, size=10):
        self.ram = [None] * size
        self.page_table = {}

    def allocate(self, process_name, content):
        """Allocates memory to an app"""
        free_slots = [i for i, x in enumerate(self.ram) if x is None]
        if not free_slots:
            return False  # Out of Memory

        # Simple allocation: just take the first available slot
        slot = free_slots[0]
        self.ram[slot] = content
        self.page_table[process_name] = slot
        return slot

    def free(self, process_name):
        """Removes given process from RAM"""
        if process_name in self.page_table:
            slot = self.page_table[process_name]
            self.ram[slot] = None
            del self.page_table[process_name]


class FileSystem:
    def __init__(self, size=20):
        self.disk = [None] * size
        self.inodes = {}

    def save(self, filename, content):
        chunks = list(content)
        needed = len(chunks)
        free_indices = [i for i, x in enumerate(self.disk) if x is None]

        if len(free_indices) < needed:
            return False  # Disk Full

        allocated = []
        for i in range(needed):
            idx = free_indices[i]
            self.disk[idx] = chunks[i]
            allocated.append(idx)

        self.inodes[filename] = allocated
        return True

    def read(self, filename):
        if filename not in self.inodes:
            return None
        indices = self.inodes[filename]
        return "".join([self.disk[i] for i in indices])

    def delete(self, filename):
        if filename in self.inodes:
            indices = self.inodes[filename]
            for i in indices:
                self.disk[i] = None
            del self.inodes[filename]
            return True
        return False


# ======================== #
# 2. THE KERNEL (The Boss) #
# ======================== #


class Kernel:
    def __init__(self):
        self.memory = MemoryManager()
        self.fs = FileSystem()
        self.scheduler_queue = deque()

    def boot(self):
        print(" [BIOS] Checking Hardware...", end="")
        time.sleep(0.5)
        print(" OK")
        print(" [KERNEL] Initializing Memory...", end="")
        time.sleep(0.5)
        print(" OK")
        print(" [KERNEL] Mounting FileSystem...", end="")
        time.sleep(0.5)
        print(" OK")
        print("\n--- Welcome to PyOS v1.0 ---\n")

    def run_process(self, name, duration):
        # 1. Load into RAM
        ram_slot = self.memory.allocate(name, "ACTIVE_DATA")
        if ram_slot is False:
            print(f" [ERROR] Out of Memory! Cannot start {name}.")
            return

        # 2. Add to CPU Schedule
        self.scheduler_queue.append({"name": name, "time": int(duration)})
        print(f" [KERNEL] Process '{name}' started (PID: {ram_slot})")

        # 3. Run Scheduler (Simplified: runs immediately)
        self._execute_schedule()

    def _execute_schedule(self):
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
        if self.fs.save(fname, data):
            print(f" [IO] Saved '{fname}' successfully.")
        else:
            print(" [IO] Error: Disk Full.")

    def sys_read(self, fname):
        data = self.fs.read(fname)
        if data:
            print(f" [IO] READ OUTPUT: {data}")
        else:
            print(f" [IO] Error: File '{fname}' not found.")


# ================ #
# 3. THE SHELL (UI)#
# ================ #
def shell():
    os = Kernel()
    os.boot()

    while True:
        try:
            cmd = input("user@pyos:~$ ").strip().split()
            if not cmd:
                continue

            op = cmd[0].lower()

            if op == "exit":
                print("Shutting down...")
                break

            elif op == "run":
                # usage: run <app_name> <seconds>
                if len(cmd) < 3:
                    print("Usage: run <name> <seconds>")
                    continue
                os.run_process(cmd[1], cmd[2])

            elif op == "write":
                # usage: write <filename> <content>
                if len(cmd) < 3:
                    print("Usage: write <filename> <content>")
                    continue
                os.sys_write(cmd[1], " ".join(cmd[2:]))

            elif op == "read":
                # usage: read <filename>
                if len(cmd) < 2:
                    print("Usage: read <filename>")
                    continue
                os.sys_read(cmd[1])

            elif op == "status":
                print(f"RAM Usage: {os.memory.ram}")
                print(f"Disk State: {os.fs.disk}")

            else:
                print(f"Unknown command: {op}")

        except KeyboardInterrupt:
            print("\nForce Shutdown.")
            break


if __name__ == "__main__":
    shell()
