class Question:
    def __init__(self, question: str, correct_answer: int, answers: list[str]):
        self._question = question
        self._correct_answer = correct_answer
        self._answers = answers
    
    def get_question(self):
        return self._question
    
    def get_answers(self):
        return self._answers

    def get_correct_answer(self):
        return self._correct_answer
 