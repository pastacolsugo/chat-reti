import string

class Player:
    def __init__(self, ip: string, socket, name: string, score: int = 0):
        self._ip = ip
        self._socket = socket
        self._name = name
        self._score = score

    def get_socket(self):
        return self._socket
    
    def get_ip(self):
        return self._ip
    
    def get_name(self):
        return self._name

    def get_score(self):
        return self._score
    
    def add_point(self):
        self._score += 1
    
    def remove_point(self):
        self._score -= 1
    
    def zero_score(self):
        self._score = 0

class PlayerState:
    def __init__(self, score:int = 0) -> None:
        self._score = score
        self._has_answered_option = False
        self._