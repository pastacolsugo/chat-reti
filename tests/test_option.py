import unittest
from src.option import OptionAnswer, OptionQuestion

class TestOption(unittest.TestCase):
    def test_option_answer(self):
        option = OptionAnswer("Forchetta", True)
        self.assertTrue(option.get_answer() == "Forchetta")
        self.assertTrue(option.is_correct())

        option = OptionAnswer("Banana", False)
        self.assertTrue(option.get_answer() == "Banana")
        self.assertFalse(option.is_correct())
    
    def test_option_question(self):
        option_question = OptionQuestion(\
            question = "In quante fette va tagliata la pizza?",\
            answers = [\
                OptionAnswer("4", False),\
                OptionAnswer("6", True),\
                OptionAnswer("La mangio intera", True)\
            ])
        self.assertTrue(option_question.get_question() == "In quante fette va tagliata la pizza?")
        self.assertTrue(len(option_question.get_answers()) == 3)
        answers = option_question.get_answers()
        for a in answers:
            self.assertTrue(type(a) is OptionAnswer)
        self.assertTrue(answers[0].get_answer() == "4")
        self.assertFalse(answers[0].is_correct())

        self.assertTrue(answers[1].get_answer() == "6")
        self.assertTrue(answers[1].is_correct())

        self.assertTrue(answers[2].get_answer() == "La mangio intera")
        self.assertTrue(answers[2].is_correct())

if __name__ == '__main__':
    unittest.main()