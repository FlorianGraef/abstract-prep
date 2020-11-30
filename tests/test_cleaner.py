import shelve
import pytest
from abstract_prep import cleaner


@pytest.fixture(scope="session")
def test_file(tmpdir_factory):
    tf_str = "123 ABC to"
    tf = tmpdir_factory.mktemp("test_data").join("test.txt")
    with open(tf) as tfw:
        tfw.write(tf_str)
    return tf


def test_parse_line():
    aid, abstract = cleaner.parse_line('1234567 "Test"')
    assert aid == "1234567"
    assert abstract == "Test"


def test_parse_line_stopwords():
    aid, abstract = cleaner.parse_line('1234567 "Test, to stop"')
    assert aid == "1234567"
    assert abstract == "Test stop"


def test_parse_file(tmpdir):
    f1 = tmpdir.mkdir("mydir").join("testfile.txt")
    f1.write("123 ABC to")

    assert f1.read() == "123 ABC to"
    with shelve.open("adb") as adb:
        result = cleaner.parse_file(f1, adb)
        assert "123" in result.keys()
        assert result["123"] == "ABC"
