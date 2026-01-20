import pytest
from pyos.memory import MemoryManager


@pytest.fixture
def mem_mgr():
    return MemoryManager(size=5)


def test_initialization(mem_mgr):
    assert len(mem_mgr.ram) == 5
    assert mem_mgr.page_table == {}


def test_allocate_success(mem_mgr):
    slot = mem_mgr.allocate("proc1", "DATA")
    assert slot == 0
    assert mem_mgr.ram[0] == "DATA"
    assert mem_mgr.page_table["proc1"] == 0


def test_allocate_oom(mem_mgr):
    # Fill RAM
    for i in range(5):
        mem_mgr.allocate(f"p{i}", "D")

    assert mem_mgr.allocate("overflow", "D") is False
    assert "overflow" not in mem_mgr.page_table


def test_allocate_finds_first_free(mem_mgr):
    mem_mgr.allocate("p1", "D1")  # slot 0
    mem_mgr.allocate("p2", "D2")  # slot 1
    mem_mgr.free("p1")  # frees slot 0

    slot = mem_mgr.allocate("p3", "D3")
    assert slot == 0
    assert mem_mgr.ram[0] == "D3"
    assert mem_mgr.page_table["p3"] == 0


def test_free_success(mem_mgr):
    mem_mgr.allocate("p1", "D")
    mem_mgr.free("p1")
    assert "p1" not in mem_mgr.page_table
    assert mem_mgr.ram[0] is None


def test_free_non_existent(mem_mgr):
    # Should not raise error
    mem_mgr.free("ghost")
