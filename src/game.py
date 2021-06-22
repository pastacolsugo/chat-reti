import random
from game_state_enum import GameState
from player import Player
from option import OptionAnswer, OptionQuestion
from question import Question
from game_config import GameConfig

class Game:
    _players_question = {} # player_name:str -> Question
    _round_option: OptionQuestion

    def __init__(self, game_config: GameConfig):
       self._game_config = game_config
       self._players = {}   # player_name:str -> Player
       self._game_state = GameState.NOT_PLAYING_ROUND
    
    def start_game(self):
        if len(self._players) < 1:
            return False
        
        self._zero_players_score()
        self._round_option = random.choice(self._game_config.get_options())
        return self._round_option
        
    def choose_option(self, player_name: str, chosen_answer: str):
        if not self._is_playing(player_name):
            print(f'Error: {player_name} is not playing.')
            return

        self._players[player_name].set_option_answered()
        
        for a in self._round_option.get_answers():
            if a.get_answer() == chosen_answer and not a.is_correct():
                self.kick_player(player_name)
                return
    
    def add_player(self, new_player : Player):
        for p in self._players:
            if new_player.get_name() == p.get_name():
                # TODO: improve error handling
                print("ERROR(add_player): Player name already in use, choose another")

        self._players.append(new_player)

    def kick_player(self, player_name):
        if player_name == "":
            return False
        
        if len(self._players) == 0:
            return False
        
        for i, p in enumerate(self._players):
            if p.get_name() == player_name:
                del self._players[i]
                return 
     
    def answer_question(self, player_name: str, answer: int):
        if not self._is_playing(player_name):
            print(f'Error: {player_name} is not playing.')
            return
        
        if self._players_question[player_name].get_correct_answer() == answer:
            self._players[player_name].add_point()
        else:
            self._players[player_name].remove_point()

    def stop_game(self):
        pass
  
    def is_game_running(self):
        pass
    
    def _is_playing(self, player_name: str):
        pass

    def _zero_players_score(self):
        for p in self._players:
            p.zero_score()