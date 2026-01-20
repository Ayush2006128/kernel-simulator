class MemoryManager:
    """
    Manages the Random Access Memory (RAM) for the operating system.

    Attributes:
        ram (list): A list representing the memory slots.
        page_table (dict): A mapping of process names to memory slots.
    """

    def __init__(self, size=10):
        """
        Initialize the MemoryManager.

        Args:
            size (int, optional): The total number of memory slots. Defaults to 10.
        """
        self.ram = [None] * size
        self.page_table = {}

    def allocate(self, process_name, content):
        """
        Allocates memory to a specific process.

        Finds the first available free slot in RAM and assigns it to the process.

        Args:
            process_name (str): The name of the process requesting memory.
            content (any): The content/data associated with the process.

        Returns:
            int or bool: The index of the allocated slot if successful, False if Out of Memory.
        """
        free_slots = [i for i, x in enumerate(self.ram) if x is None]
        if not free_slots:
            return False  # Out of Memory

        # Simple allocation: just take the first available slot
        slot = free_slots[0]
        self.ram[slot] = content
        self.page_table[process_name] = slot
        return slot

    def free(self, process_name):
        """
        Frees the memory allocated to a process.

        Args:
            process_name (str): The name of the process to remove from RAM.
        """
        if process_name in self.page_table:
            slot = self.page_table[process_name]
            self.ram[slot] = None
            del self.page_table[process_name]
