import unittest
from src.question import Question

class TestQuestion(unittest.TestCase):
    def test_question(self):
        answers_1 = ["300 hamburger", "0 hamburger", "sistema metrico", "maledetti americani"]
        question_1 = Question(question="Quanto e' lungo un campo da calcio se misurato in hamburger?", \
            answers= answers_1, correct_answer=3)
        self.assertTrue(question_1.get_question() == "Quanto e' lungo un campo da calcio se misurato in hamburger?")
        self.assertTrue(question_1.get_answers() == answers_1)
        self.assertTrue(question_1.get_correct_answer() == 3)

if __name__ == '__main__':
    unittest.main()

