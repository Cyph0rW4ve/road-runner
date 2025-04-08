import unittest
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app, get_db, CargoTypes, Trucks
from unittest.mock import MagicMock, patch
from app.drivertimecalculator import DriverTimeCalculator
from pydantic import BaseModel


client = TestClient(app)


class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()

        self.mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [
            CargoTypes(
                id="C001", cargo_name="Food", cargo_type="Perishable"), CargoTypes(
                id="C002", cargo_name="Steel", cargo_type="Heavy")]

        app.dependency_overrides[get_db] = lambda: self.mock_db

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_cargo_types(self):
        response = client.get("/cargo_types/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("cargo_name", data[0])
        self.assertEqual(data[0]["cargo_name"], "Food")

    def test_trucks(self):
        self.mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [
            Trucks(
                id="T001",
                brand="Volvo",
                name="BigTruck",
                fuel_tank=400,
                liters_per_100km=30,
                max_weight=20000),
            Trucks(
                id="T002",
                brand="Scania",
                name="FastTruck",
                fuel_tank=500,
                liters_per_100km=25,
                max_weight=25000)]

        response = client.get("/trucks/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("brand", data[0])
        self.assertEqual(data[0]["brand"], "Volvo")

    def test_google_maps_api_connection(self):
        api_key = "AIzaSyBT_yW-Nz6zIbKidF_WgaKG3o17xeOI6-c"
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": "Berlin",
            "key": api_key
        }

        response = requests.get(url, params=params)

        self.assertEqual(
            response.status_code,
            200,
            f"Fehler beim Aufruf: {
                response.status_code}")
        data = response.json()
        self.assertIn("results", data, "Antwort enthält keine 'results'")
        self.assertGreater(len(data["results"]), 0,
                           "Keine Ergebnisse zurückgegeben")

    @patch('requests.get')
    def test_mock_google_maps_api_connection(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": ["some result"]
        }

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": "Berlin",
            "key": "fake_api_key"
        }

        response = requests.get(url, params=params)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)


class TestCalculateTime(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock()
        self.driver.get_remaining_drive_time.return_value = 36000  # 10 hours in seconds
        self.driver.update_free_drive_time = MagicMock()
        self.driver.small_break = MagicMock()
        self.driver.big_break = MagicMock()

        self.calculator = DriverTimeCalculator()
        self.calculator.driver = self.driver
        self.calculator.drivable_seconds_per_day = 32400  # 9 hours in seconds

    def test_calculate_time_exceeds_drive_time(self):
        driver_id = "0001"
        calculated_route_duration = 36000  # 10 hours in seconds
        needed_stops = 0
        # 36000 + 2700 (small break) + 39600 (big break) = 78300
        expected_total_duration = 78300

        self.driver.get_remaining_drive_time.return_value = 32400  # 9 hours available

        total_duration = self.calculator.calculate_time(
            driver_id, calculated_route_duration, needed_stops)

        self.assertEqual(total_duration, expected_total_duration)


if __name__ == '__main__':
    unittest.main()
