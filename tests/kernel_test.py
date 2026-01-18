import pytest
from unittest.mock import patch
from kernel import Kernel


@pytest.fixture
def kernel():
    k = Kernel()
    # Replace subsystems with mocks if we want isolated unit tests,
    # but integration testing the simple subsytems is also fine.
    # For this, let's stick to real subsystems but mock time/print.
    return k


@patch("time.sleep")
@patch("kernel.print")
def test_boot(mock_print, mock_sleep, kernel):
    kernel.boot()
    assert mock_sleep.call_count == 3
    # Check for some expected print calls
    assert any("Welcome to PyOS" in str(c) for c in mock_print.call_args_list)


@patch("time.sleep")
@patch("kernel.print")
def test_run_process_success(mock_print, mock_sleep, kernel):
    kernel.run_process("app1", 3)

    # Process should have run and finished (since _execute_schedule runs immediately)
    # So it should be removed from memory eventually
    assert "app1" not in kernel.memory.page_table
    assert len(kernel.scheduler_queue) == 0
    # Verify it actually ran
    assert any("Finished" in str(c) for c in mock_print.call_args_list)


@patch("time.sleep")
@patch("kernel.print")
def test_run_process_oom(mock_print, mock_sleep, kernel):
    # Fill memory artificially
    kernel.memory.ram = ["FULL"] * len(kernel.memory.ram)

    kernel.run_process("app_oom", 1)

    # Should not be in queue or table
    assert "app_oom" not in kernel.memory.page_table
    assert len(kernel.scheduler_queue) == 0


@patch("time.sleep")
@patch("kernel.print")
def test_run_process_invalid_duration(mock_print, mock_sleep, kernel):
    kernel.run_process("bad_time", "invalid")

    assert "bad_time" not in kernel.memory.page_table
    assert len(kernel.scheduler_queue) == 0


def test_sys_write_read(kernel):
    # Integration test for syscalls
    with patch("kernel.print") as mock_print:
        kernel.sys_write("file1", "content")
        assert kernel.fs.read("file1") == "content"

        kernel.sys_read("file1")
        # Verify read output was printed
        assert any("content" in str(args) for args, kwargs in mock_print.call_args_list)


def test_sys_read_not_found(kernel):
    with patch("kernel.print") as mock_print:
        kernel.sys_read("ghost_file")
        assert any(
            "not found" in str(args) for args, kwargs in mock_print.call_args_list
        )
