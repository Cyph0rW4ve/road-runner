import unittest
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import MagicMock, patch
from drivertimecalculator import DriverTimeCalculator


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

#   def test_owned_trucks(self):
#       response_owned_trucks = self.client.get("/owned_trucks")
#       owned_trucks = response_owned_trucks.json()
#       self.assertIsInstance(owned_trucks, list)
#       if owned_trucks:
#           self.assertIn("id", owned_trucks[1])
#           self.assertIn("truck_id", owned_trucks[1])
#           self.assertIn("current_driver", owned_trucks[1])

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

   # def test_drive_duration(self):      # richtige dauer bei Auftrag von 10 Std
   #     class DriverTimeCalculator(unittest.TestCase):

    def test_calculate_time_shorter_than_remaining_time(self):
        #given
        driver_id = "D001"
        remaining_delivery_time = 36000  # 10 Stunden
        remaining_drive_time = 32400
        needed_stops = 0
        obj = DriverTimeCalculator()  # <- Ersetze das mit dem Klassennamen, in dem calculate_time steckt
        #then
        result = obj.calculate_time(driver_id, remaining_delivery_time, needed_stops)
        #when
        expectedResult = 78900
        self.assertEqual(result, expectedResult)


if __name__ == '__main__':
    unittest.main()