from time import sleep

class Timer:
    def __init__(self, duration: int):
        self._duration = duration
        self._is_timer_over = False
        self._time_left = self._duration

    def start(self):
        self._time_left = self._duration
        while self._time_left > 0 and not bool(self._is_timer_over):
            sleep(1)
            self._time_left -= 1
        if self._time_left == 0:
            self._is_timer_over = True

    # TODO: @alicemastrilli evaluate the need for the stop method.
    # Can it be called? Do we need it?
    def stop(self):
        self._is_timer_over = True

    def get_remaining_time(self):
        return self._time_left

    def is_timer_over(self):
        return self._is_timer_over
