class Driver:
    def __init__(self):
        self.id: str = "D001"
        self.free_drive_time: int = 32400
        self.open_break_duration: int = 0
        self.available_for_next_job: bool = None

    def read_stats(self):
        pass

    def update_stats_to_db(self):
        pass

    def new_driver(self, new_id: str):
        pass

    def update_free_drive_time(self, seconds):
        self.free_drive_time -= seconds

    def small_break(self):
        self.open_break_duration += 45 * 60# 45 min in seconds

    def big_break(self):
        self.open_break_duration += 11 * 60 * 60# 11 hours in seconds

    def get_remaining_drive_time(self):
        return self.free_drive_time

    def get_break_duration_sum(self):
        return self.open_break_duration
