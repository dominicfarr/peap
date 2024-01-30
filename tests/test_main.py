import unittest
from src import main

class TestMain(unittest.TestCase):
    def test_hello_world(self):
        result = main.say_hello()
        self.assertEqual(result, "Hello, World")