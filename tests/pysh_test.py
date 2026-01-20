import pytest
from unittest.mock import MagicMock, patch
from pyshell.pysh import PyShell


@pytest.fixture
def shell():
    return PyShell()


@patch("rich.prompt.Prompt.ask")
@patch("pysh.print")
@patch("kernel.Kernel.boot")  # Mock boot to save time
def test_shell_exit(mock_boot, mock_print, mock_ask, shell):
    # Simulate user typing 'exit'
    mock_ask.side_effect = ["exit"]

    shell.run()

    assert mock_boot.called
    assert mock_ask.call_count == 1


@patch("rich.prompt.Prompt.ask")
@patch("pysh.print")
@patch("kernel.Kernel.boot")
def test_shell_commands(mock_boot, mock_print, mock_ask, shell):
    # Simulate a sequence of commands
    mock_ask.side_effect = [
        "write test.txt hello",
        "read test.txt",
        "status",
        "run myproc 1",
        "unknown_cmd",
        "",  # Empty input
        "exit",
    ]

    # We also need to mock kernel methods to verify they are called,
    # or rely on integration behavior if we want to test that.
    # Let's spy on the kernel methods.
    shell.kernel.sys_write = MagicMock()
    shell.kernel.sys_read = MagicMock()
    shell.kernel.run_process = MagicMock()

    shell.run()

    shell.kernel.sys_write.assert_called_with("test.txt", "hello")
    shell.kernel.sys_read.assert_called_with("test.txt")
    shell.kernel.run_process.assert_called_with("myproc", "1")

    assert mock_ask.call_count == 7


@patch("rich.prompt.Prompt.ask")
@patch("pysh.print")
def test_shell_usage_checks(mock_print, mock_ask, shell):
    # Test incorrect usage
    shell.kernel.boot = MagicMock()
    mock_ask.side_effect = [
        "run",  # Missing args
        "write file",  # Missing content
        "read",  # Missing filename
        "exit",
    ]

    shell.run()

    # We verify that it didn't crash and handled prompts
    assert mock_ask.call_count == 4
    # Could check for usage messages in mock_print if desired
