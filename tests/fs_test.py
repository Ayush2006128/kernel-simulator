import pytest
from pyos.fs import FileSystem


@pytest.fixture
def fs():
    return FileSystem(size=10)


def test_initialization(fs):
    assert len(fs.disk) == 10
    assert fs.inodes == {}
    assert all(block is None for block in fs.disk)


def test_save_success(fs):
    filename = "test.txt"
    content = "abc"
    assert fs.save(filename, content) is True
    assert fs.inodes[filename] == [0, 1, 2]
    assert fs.disk[0] == "a"
    assert fs.disk[1] == "b"
    assert fs.disk[2] == "c"


def test_save_full_disk(fs):
    # Fill disk
    fs.save("fill", "a" * 10)
    assert fs.save("fail", "b") is False
    assert "fail" not in fs.inodes


def test_save_fragmented(fs):
    fs.save("f1", "aa")
    fs.save("f2", "bb")
    fs.delete("f1")
    # Disk should have gaps at 0, 1. f2 is at 2, 3.
    # Saving "ccc" needs 3 blocks. Should take 0, 1, and 4.
    assert fs.save("f3", "ccc") is True
    assert fs.inodes["f3"] == [0, 1, 4]
    assert fs.disk[0] == "c"
    assert fs.disk[1] == "c"
    assert fs.disk[4] == "c"


def test_read_success(fs):
    fs.save("read_me", "hello")
    assert fs.read("read_me") == "hello"


def test_read_not_found(fs):
    assert fs.read("non_existent") is None


def test_delete_success(fs):
    fs.save("del_me", "data")
    assert fs.delete("del_me") is True
    assert "del_me" not in fs.inodes
    # Verify disk blocks are freed
    assert all(block is None for block in fs.disk)


def test_delete_not_found(fs):
    assert fs.delete("ghost") is False
