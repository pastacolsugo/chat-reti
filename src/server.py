from time import sleep
import threading
import socket
import json
import random

HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080
# CONFIG_FILE_PATH = './config.json'
CONFIG_FILE_PATH = '/Users/sugo/git/chat-reti/src/config.json'
with open(CONFIG_FILE_PATH, 'r') as config_file:
    GAME_CONFIG = json.load(config_file)

server_socket = None
client_sockets = {}
next_connection_id = 0
has_game_started = False
is_game_over = False
ranking = {}

cancer_flag = False

def open_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST_ADDR, HOST_PORT))
    server_socket.listen(5) # allowed connection attempts

    threading._start_new_thread(accept_new_clients, (server_socket,))

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
        threading._start_new_thread(handle_player_connection, (id,))

def get_next_connection_id():
    global next_connection_id
    id = next_connection_id
    next_connection_id += 1
    return id

def handle_player_connection(id):
    global is_game_over, GAME_CONFIG, ranking, has_game_started, cancer_flag
    score = 0
    player_socket = client_sockets[id]['socket']

    # read name
    msg = player_socket.recv(4096).decode() 
    if not msg:
        # TODO: exit gracefully
        return
    player_name = json.loads()['player_name']
    if not player_name:
        print ('no player name')
        return
    print(f'Player connected: {player_name}')

    # assign role
    player_role = random.choice(GAME_CONFIG['roles'])
    msg = {"role" : player_role}
    player_socket.send(json.dumps(msg).encode())

    # wait for game to start
    while not has_game_started:
        try:
            start_msg = player_socket.recv(4096, socket.MSG_DONTWAIT).decode()
            if start_msg and start_msg == "start_game":
                has_game_started = True
            else:
                return
        except Exception as e:
            pass
        sleep(0.1)

    print('Game started!')

    # serve option
    option = random.choice(GAME_CONFIG['options'])
    player_socket.send(json.dumps(option).encode())
    
    print('Option served, waiting for player choice.')

    # wait for user choice
    # {'choice' : 'scelta'}
    msg = player_socket.recv(4096).decode()
    if not msg:
        return # TODO: handle exit
    player_choice = json.loads(msg)['choice']

    print(player_choice)

    print('Choice received. Evaluating...')

    # evaluate user choice
    for choice in option['option_answers']:
        if choice['option'] == player_choice and choice['correct']:
            break
    else:
        # TODO: handle exit
        return
    
    
    # while (number of questions < X):
    while score < GAME_CONFIG['winning_score'] and not is_game_over:
        # serve question
        question = random.choice(GAME_CONFIG['questions'])
        player_socket.send(json.dumps(question).encode())

        # wait for answer
        msg = player_socket.recv(4096).decode()
        if not msg:
            return

        # expected object
        # {'answer' : '3'}
        player_answer = json.loads(msg)['answer']

        print("player_answer")
        print(player_answer)
        
        # check answer and assign points
        if player_answer == question['correct_answer']:
            score += 1
        else:
            score -= 1 
        
        # send new score to client
        score_update = {'score' : score}
        player_socket.send(json.dumps(score_update).encode())

    # check if I won
    if not is_game_over and score >= GAME_CONFIG['winning_score']:
        is_game_over = True

    # add my score to the ranking
    ranking[player_name] = score
    
    # wait for all other threads to add their names
    while len(ranking) < len(client_sockets):
        sleep(0.1)
    

    # generate sorted ranking
    sorted_ranking = dict(sorted(ranking.items(), reverse=True, key=lambda item: item[1]))

    # serialize ranking
    serialized_ranking = ""
    for key in sorted_ranking:
        serialized_ranking += f'{key}: {sorted_ranking[key]}'
    
    # send ranking
    player_socket.send(serialized_ranking.encode())

    # close connection
    player_socket.close()

    # exit
    cancer_flag = True

def start_server():
    print('Ingegneria e Scienze Informatiche - UniBo')
    print('Progetto Traccia #3 - Esame di Reti')
    print('A. Conti, A. Mastrilli, U. Baroncini')
    open_socket()
    
    while not cancer_flag:
        sleep(0.1)
        # TODO: close once done


start_server()