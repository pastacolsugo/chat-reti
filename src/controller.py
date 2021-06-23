from time import sleep
import threading
from game import Game
import socket
import json
import random

HOST_ADDR = '127.0.0.1'
HOST_PORT = '8080'
CONFIG_FILE_PATH = 'config.json'
with open(CONFIG_FILE_PATH, 'r') as config_file:
    GAME_CONFIG = json.load(config_file)

server_socket = None
client_sockets = {}
next_connection_id = 0
has_game_started = False

def open_socket(self):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST_ADDR, HOST_PORT))
    server_socket.listen(5) # allowed connection attempts

    threading._start_new_thread(accept_new_clients, (server_socket))

def accept_new_clients(server_socket):
    global client_sockets
    while True:
        client_socket, client_addr = server_socket.accept()

        # genera un ConnectionID
        id = get_next_connection_id()
        
        # memorizza il socket e i dati utili in una struttura, usando ConnectionID come identificativo
        client_sockets[id] = {
            'socket': client_socket,
            'address': client_addr,
            'player_name': '',
            'id': id
        }

        # spawna un nuovo thread e gli da in gestione quella connessione (tramite ConnectionID)
        threading._start_new_thread(handle_player_connection, (id))

def get_next_connection_id():
    global next_connection_id
    id = next_connection_id
    next_connection_id += 1
    return id

def handle_player_connection(id):
    player_socket = client_sockets[id]['socket']

    # read name
    player_name = player_socket.recv(4096)

    # assign role
    player_role = random.choice(GAME_CONFIG['roles'])
    player_socket.send(f'role:{player_role}')

    # wait for game to start
    while not has_game_started:
        sleep(0.1)

    
    option = random.choice(GAME_CONFIG['options'])
    player_socket.send(json.)
    # serve option
    # wait for user choice
    # evaluate user choice
    # while (number of questions < X):
    #   serve question
    #   wait for answer
    #   check answer
    #   assign points
    # send ranking
    # close connection
    # exit

class ChatController():
    def __init__(self, question_file_path):
        self._game_data = DataParser(_game_data_file_path).get_game_data()
        self._game = Game(self._game_data)
        self._clients = {} # key:conn_id -> (client_socket, client_addr, Player)
        self._next_connection_id = 0
         
    def start_game(self):
        self._game.start_game()
    
    def stop_game(self):
        self._game.stop_game()

    def is_game_running(self):
        return self._game.is_game_running()
    
    def is_game_started(self):

    def _get_option(self):
        return self._game_data.options[0]

    def _get_config(self, path):
        with open(path, 'r') as file:
            self._data = json.loads(file)