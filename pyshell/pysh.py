from pyos.kernel import Kernel
from rich import print
from rich.prompt import Prompt


class PyShell:
    """
    The interactive shell for PyOS.

    Attributes:
        kernel (Kernel): The operating system kernel instance.
    """

    def __init__(self):
        """
        Initialize the PyShell and the Kernel.
        """
        self.kernel = Kernel()

    def run(self):
        """
        Starts the shell loop, accepting user commands.
        """
        self.kernel.boot()

        while True:
            try:
                cmd_input = Prompt.ask(
                    "[green]monty@pyos[/green][blue]:[/blue]~$"
                ).strip()
                if not cmd_input:
                    continue

                cmd = cmd_input.split()
                op = cmd[0].lower()

                if op == "exit":
                    print("Shutting down...")
                    break

                elif op == "run":
                    # usage: run <app_name> <seconds>
                    if len(cmd) < 3:
                        print("[bold]Usage:[/bold] run <name> <seconds>")
                        continue
                    self.kernel.run_process(cmd[1], cmd[2])

                elif op == "write":
                    # usage: write <filename> <content>
                    if len(cmd) < 3:
                        print("[bold]Usage:[/bold] write <filename> <content>")
                        continue
                    # Join the rest of the arguments to form content
                    content = " ".join(cmd[2:])
                    self.kernel.sys_write(cmd[1], content)

                elif op == "read":
                    # usage: read <filename>
                    if len(cmd) < 2:
                        print("[bold]Usage:[/bold] read <filename>")
                        continue
                    self.kernel.sys_read(cmd[1])

                elif op == "status":
                    print(f"[bold]RAM Usage:[/bold] {self.kernel.memory.ram}")
                    print(f"[bold]Disk State:[/bold] {self.kernel.fs.disk}")

                else:
                    print(f"[red]Unknown command: {op}[/red]")

            except KeyboardInterrupt:
                print("\n[red]Force Shutdown.[/red]")
                break
