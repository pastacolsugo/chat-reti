import string
from question_parser import QuestionParser # TODO: Import correct module

class ChatController():
    def __init__(self, question_file_path):
        self._question_file_path = question_file_path
        self._game_data = DataParser(_game_data_file_path).get_game_data()
        self._game = Game(self._game_data)


    
    def start_game(self):
        self._game.start_game()
    
    def stop_game(self):
        self._game.stop_game()

    def is_game_running(self):
        return self._game.is_game_running()
    
    def is_round_running(self):

    
    def get_remaining_time(self):