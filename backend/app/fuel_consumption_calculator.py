import re


class FuelConsumptionCalculator:
    def calculate_stops(self, total_distance, fuel_tank, consumption):
        truck_range = self.get_truck_range(fuel_tank, consumption)
        filtered_distance = float(
            re.search(
                r"\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?",
                total_distance).group().replace(
                ",",
                ""))
        return int(filtered_distance / truck_range)

    def get_truck_range(self, fuel_tank, consumption):
        return fuel_tank / consumption * 100
