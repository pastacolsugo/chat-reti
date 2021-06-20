import string


class Player:
    def __init__(self, ip: string, socket, player_name: string, score: int):
        self.__ip = ip
        self.__socket = socket
        self.__playerName = player_name
        self.__score = score

    def get_socket(self):
        return self.__socket
