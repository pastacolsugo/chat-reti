from question import Question
from option import Option

class GameConfig:
    def __init__(self, questions: list[Question], \
            options: list[Option], timer_duration: int) -> None:
        self._questions = questions
        self._options = options
        self._timer_duration = timer_duration
    
    def get_timer_duration(self):
        return self._timer_duration
    
    def get_questions(self):
        return self._questions
    
    def get_options(self):
        return self._options
