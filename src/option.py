class Option:
    def __init__(self, option: str, is_correct: bool):
        self._option = option
        self._is_correct = is_correct

    def get_option(self):
        return self._option

    def is_correct(self):
        return self._is_correct

