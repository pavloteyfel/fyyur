import unittest
from flask_testing import TestCase
from app import app


class TestApp(TestCase):
    def create_app(self):
        return app

    def test_main_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_venues_endpoint(self):
        response = self.client.get("/venues")
        self.assertEqual(response.status_code, 200)

    def test_artists_endpoint(self):
        response = self.client.get("/artists")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
