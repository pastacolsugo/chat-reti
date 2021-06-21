class Question:
    def __init__(self, question: str, correctAnswer: int, answers):
        self._question = question
        self._correctAnswer = correctAnswer
        self._answers = answers
    
    def getQuestion(self):
        return self._question
    
    def getAnswers(self):
        return self._answers

    def getCorrectAnswer(self):
        return self._correctAnswer

        