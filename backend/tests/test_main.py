import unittest
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch
from app.drivertimecalculator import DriverTimeCalculator



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


    def test_google_maps_api_connection(self):
        api_key = "AIzaSyBT_yW-Nz6zIbKidF_WgaKG3o17xeOI6-c"
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": "Berlin",
            "key": api_key
        }

        response = requests.get(url, params=params)

        self.assertEqual(response.status_code, 200, f"Fehler beim Aufruf: {response.status_code}")
        data = response.json()
        self.assertIn("results", data, "Antwort enthält keine 'results'")
        self.assertGreater(len(data["results"]), 0, "Keine Ergebnisse zurückgegeben")
    
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

        total_duration = self.calculator.calculate_time(driver_id, calculated_route_duration, needed_stops)

        self.assertEqual(total_duration, expected_total_duration)



if __name__ == '__main__':
    unittest.main()