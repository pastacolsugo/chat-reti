import string

class Option:
    def __init__(self, option: string, isCorrect: bool):
        self._option = option
        self._isCorrect = isCorrect

    def get_option(self):
        return self._option

    def is_correct(self):
        return self._isCorrect


#PROVA
#option = Option("aliceisbeautiful", True)
#print(Option.getOption(option))
#print(Option.isCorrect(option))

