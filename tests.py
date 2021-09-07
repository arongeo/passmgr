import app
import database
import crypt
import menu
import auth

def test_hash():
    assert "test" != crypt.hash("test")

