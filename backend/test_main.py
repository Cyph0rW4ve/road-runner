import unittest
from main import *
from fastapi import FastAPI
from fastapi.testclient import TestClient

class TestDatabaseConnection(unittest.TestCase):
    client = TestClient(app)
    def test_cargo_types(self):
        response_cargo = self.client.get("/cargo_types")
        cargo_types = response_cargo.json()
        self.assertEqual(response_cargo.status_code, 200)
        self.assertIsInstance(cargo_types, list)
        if cargo_types:
            self.assertIn("id", cargo_types[1])
            self.assertIn("cargo_name", cargo_types[1])
            self.assertIn("cargo_type", cargo_types[1])

    def test_trucks(self):
        response_trucks = self.client.get("/trucks")
        trucks = response_trucks.json()
        self.assertIsInstance(trucks, list)
        if trucks:
            self.assertIn("id", trucks[1])
            self.assertIn("name", trucks[1])
            self.assertIn("fuel_tank", trucks[1])

    def test_owned_trucks(self):
        response_owned_trucks = self.client.get("/owned_trucks")
        owned_trucks = response_owned_trucks.json()
        self.assertIsInstance(owned_trucks, list)
        if owned_trucks:
            self.assertIn("id", owned_trucks[1])
            self.assertIn("truck_id", owned_trucks[1])
            self.assertIn("current_driver", owned_trucks[1])

if __name__ == '__main__':
    unittest.main()