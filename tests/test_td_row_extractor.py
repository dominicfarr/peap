import pytest

@pytest.mark.parametrize("line, expected", [("line1","line1")])
def test_extractor(line, expected):
    assert line == expected