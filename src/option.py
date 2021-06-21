class Option:
    def __init__(self, option: str, isCorrect: bool):
        self._option = option
        self._isCorrect = isCorrect

    def get_option(self):
        return self._option

    def is_correct(self):
        return self._isCorrect

