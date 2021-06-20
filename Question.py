import string

class Question:

    def __init__(self, question: string, correctAnswer: int, answers):
        self.__question = question
        self.__correctAnswer = correctAnswer
        self.__answers = answers
    
    def getQuestion(self):
        return self.__question
    
    def getAnswers(self):
        return self.__answers

    def getCorrectAnswer(self):
        return self.__correctAnswer

        