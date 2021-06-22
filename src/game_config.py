from question import Question
from option import Option

class GameConfig:
    def __init__(self, questions: list[Question], \
            options: list[OptionQuestions], winning_score: int) -> None:
        self._questions = questions
        self._options = options
        self._winning_score = winning_score
    
    def get_winning_score(self):
        return self._winning_score
    
    def get_questions(self):
        return self._questions
    
    def get_options(self):
        return self._options
