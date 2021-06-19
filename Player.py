import string


class Player:
    def __init__(self, ip: string, socket, player_name: string, score: int):
        self.ip = ip
        self.socket = socket
        self.playerName = player_name
        self.score = score

    def get_socket(self):
        return self.socket
