from time import sleep


class Timer:
    __isTimerOver = False

    def __init__(self, duration: int):
        self.__duration = duration

    def start_timer(self):
        while self.__duration > 0 and not bool(self.__isTimerOver):
            # print(self.__duration)
            self.__duration = self.__duration - 1
            sleep(1)
        if self.__duration == 0:
            self.__isTimerOver = True

    def stop_timer(self):
        self.__isTimerOver = True

    def get_remaining_time(self):
        return self.__duration

    def is_timer_over(self):
        return self.__isTimerOver

# PROVA
# timer = Timer(5)
# print(Timer.is_timer_over(timer))
# Timer.start_timer(timer)
# print(Timer.is_timer_over(timer))
