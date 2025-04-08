from app.driver import Driver


class DriverTimeCalculator:
    def __init__(self):
        self.drivable_seconds_per_day = 9 * 60 * 60  # 9 hours in seconds
        self.small_break = 45 * 60      # 45 minutes in seconds
        self.big_break = 11 * 60 * 60   # 11 hours in seconds
        self.driver = Driver()
        self.total_duration = 0
        self.remaining_delivery_time = 0

    def calculate_time(
            self,
            driver_id,
            calculated_route_duration,
            needed_stops):
        # self.driver.new_driver(driver_id)
        self.total_duration = calculated_route_duration
        self.remaining_delivery_time = calculated_route_duration

        # add 10m minutes to total duration for each stop
        self.total_duration += needed_stops * 10 * 60

        remaining_drive_time_today = self.driver.get_remaining_drive_time()

        if calculated_route_duration < remaining_drive_time_today:
            self.driver.update_free_drive_time(calculated_route_duration)
            # self.driver.update_stats_to_db()
            return self.total_duration

        if calculated_route_duration == remaining_drive_time_today:
            self.driver.update_free_drive_time(self.drivable_seconds_per_day)
            self.driver.small_break()
            self.driver.big_break()
            # self.driver.update_stats_to_db()
            return self.total_duration

        self.handle_first_day(remaining_drive_time_today)

        needed_full_days = int(
            calculated_route_duration /
            self.drivable_seconds_per_day)
        for i in range(0, needed_full_days):
            self.handle_full_day()

        self.handle_last_day()

        # self.driver.update_stats_to_db()
        return self.total_duration

    def handle_first_day(self, remaining_drive_time_today):
        self.remaining_delivery_time -= remaining_drive_time_today
        self.driver.small_break()
        self.driver.big_break()
        self.total_duration += self.small_break
        self.total_duration += self.big_break

    def handle_full_day(self):
        self.remaining_delivery_time -= self.drivable_seconds_per_day
        if self.remaining_delivery_time > 0:
            self.driver.small_break()
            self.driver.big_break()
            self.total_duration += 15 * 60 * 60  # seconds until end of day

    def handle_last_day(self):
        self.driver.update_free_drive_time(self.remaining_delivery_time)
