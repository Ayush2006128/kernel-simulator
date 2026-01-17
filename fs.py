class FileSystem:
    """
    Manages the file storage on a simulated disk.

    Attributes:
        disk (list): A list representing disk blocks.
        inodes (dict): A mapping of filenames to lists of allocated disk indices.
    """

    def __init__(self, size=20):
        """
        Initialize the FileSystem.

        Args:
            size (int, optional): The total number of blocks on the disk. Defaults to 20.
        """
        self.disk = [None] * size
        self.inodes = {}

    def save(self, filename, content):
        """
        Saves a file to the disk.

        Splits content into chunks and attempts to find enough free blocks.

        Args:
            filename (str): The name of the file to save.
            content (str): The content of the file.

        Returns:
            bool: True if the file was saved successfully, False if the disk is full.
        """
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
        """
        Reads a file from the disk.

        Args:
            filename (str): The name of the file to read.

        Returns:
            str or None: The content of the file if found, None otherwise.
        """
        if filename not in self.inodes:
            return None
        indices = self.inodes[filename]
        return "".join([self.disk[i] for i in indices])

    def delete(self, filename):
        """
        Deletes a file from the disk.

        Frees the allocated blocks and removes the inode entry.

        Args:
            filename (str): The name of the file to delete.

        Returns:
            bool: True if the file was deleted, False if it was not found.
        """
        if filename in self.inodes:
            indices = self.inodes[filename]
            for i in indices:
                self.disk[i] = None
            del self.inodes[filename]
            return True
        return False
