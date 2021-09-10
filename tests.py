import unittest
import app
import database
import crypt
import menu
import auth

class Testing(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(crypt.hash("test"), "3a7b0c3880ac54833abda5957dad646380a312a5b985adbe23e33a2ba6a10a3e")


if __name__ == '__main__':
    unittest.main()
