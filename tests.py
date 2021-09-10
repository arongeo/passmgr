import unittest
import app
import database
import crypt
import menu
import auth

class Testing(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(crypt.hash("test"), "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")


if __name__ == '__main__':
    unittest.main()
