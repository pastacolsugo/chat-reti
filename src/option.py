import string

class Option:
    def __init__(self, option: string, isCorrect: bool):
        self.__option = option
        self.__isCorrect = isCorrect

    def getOption(self):
        return self.__option

    def isCorrect(self):
        return self.__isCorrect


#PROVA
#option = Option("aliceisbeautiful", True)
#print(Option.getOption(option))
#print(Option.isCorrect(option))

