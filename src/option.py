class OptionAnswer:
    def __init__(self, answer: str, is_correct: bool):
        self._answer = answer
        self._is_correct = is_correct

    def get_answer(self):
        return self._answer

    def is_correct(self):
        return self._is_correct

class OptionQuestion:
    def __init__(self, question: str, answers: list[OptionAnswer]) -> None:
        self._question = question
        self._answers = answers
    
    def get_question(self):
        return self._question
    
    def get_answers(self):
        return self._answers