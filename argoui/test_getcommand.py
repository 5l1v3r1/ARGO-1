from app import generatecommand
import pytest

def test_generatecommand():
    assert generatecommand("https://github.com", 1) == "python3 ./attack.py 140.82.118.4 https://github.com 1"
