from time import sleep
import threading
import socket
import json
import random

HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080

# Set the correct path for your machine!
CONFIG_FILE_PATH = '/Users/sugo/git/chat-reti/src/config.json'
with open(CONFIG_FILE_PATH, 'r') as config_file:
    GAME_CONFIG = json.load(config_file)

server_socket = None
client_sockets = {}
next_connection_id = 0
has_game_started = False
is_game_over = False
is_ranking_ready = False
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
    global is_ranking_ready
    score = 0
    player_socket = client_sockets[id]['socket']

    # Read name
    # {'player_name' : name}
    msg = player_socket.recv(4096).decode() 
    if not msg:
        print('> Lost connection.')
        return
    player_name = json.loads(msg)['player_name']
    if not player_name:
        print ('no player name')
        return
    print(f'Player connected: {player_name}')

    # Assign role
    player_role = random.choice(GAME_CONFIG['roles'])
    msg = {"role" : player_role}
    player_socket.send(json.dumps(msg).encode())

    received_start_game_message = False
    # Wait for game to start
    while not has_game_started:
        try:
            msg = player_socket.recv(4096, socket.MSG_DONTWAIT).decode()
            if not msg:
                print(f'{player_name}> Lost connection.')
                return
            start_msg = json.loads(msg)
            if start_msg['start_game']:
                has_game_started = True
                received_start_game_message = True
            else:
                return
        except Exception as e:
            pass
        sleep(0.1)
    
    if not received_start_game_message:
        msg = {'game_started' : 'True'}
        player_socket.send(json.dumps(msg).encode())

    print(f'{player_name}Game started!')

    # Serve option
    option = random.choice(GAME_CONFIG['options'])
    player_socket.send(json.dumps(option).encode())
    
    print(f'{player_name}> Option served, waiting for player choice.')

    # Wait for user choice
    # {'choice' : 'scelta'}
    msg = player_socket.recv(4096).decode()
    if not msg:
        print(f'{player_name}> Lost connection')
    player_choice = json.loads(msg)['choice']

    print(player_choice)

    print(f'{player_name}Choice received. Evaluating...')

    # Evaluate user choice
    for choice in option['option_answers']:
        if choice['option'] == player_choice and choice['correct'] == "True":
            break
    else:
        close_connection(id)
        return
    
    # while (number of questions < X):
    while score < GAME_CONFIG['winning_score'] and not is_game_over:
        # Serve question
        question = random.choice(GAME_CONFIG['questions'])
        player_socket.send(json.dumps(question).encode())

        # Wait for answer
        msg = player_socket.recv(4096).decode()
        if not msg:
            print(f'{player_name}> Lost connection')
            return

        # expected object
        # {'answer' : '3'}
        player_answer = json.loads(msg)['answer']

        # Check answer and assign points
        if player_answer == question['correct_answer']:
            score += 1
        else:
            score -= 1 
        
        # Send new score to client
        score_update = {'score' : score}
        player_socket.send(json.dumps(score_update).encode())
        sleep(0.5)

    # Check if I won
    if not is_game_over and score >= GAME_CONFIG['winning_score']:
        is_game_over = True

    # Add my score to the ranking
    ranking[player_name] = score
    print(f'Added {player_name} score -> {score} | len(ranking){len(ranking)}, len(clients){len(client_sockets)}')
    
    if len(ranking) == len(client_sockets):
        is_ranking_ready = True
    # Wait for all other threads to add their names
    while not is_ranking_ready:
        sleep(0.1)

    # Generate sorted ranking
    sorted_ranking = dict(sorted(ranking.items(), reverse=True, key=lambda item: item[1]))

    # Serialize ranking
    serialized_ranking = ''
    for key in sorted_ranking:
        serialized_ranking += f'{key}: {sorted_ranking[key]}\n'
    msg = {'ranking': serialized_ranking}

    # Send ranking
    player_socket.send(json.dumps(msg).encode())

    # Remove client socket from data structure
    client_sockets.pop(id)

    # close connection
    player_socket.close()

def start_server():
    print('Ingegneria e Scienze Informatiche - UniBo')
    print('Progetto Traccia #3 - Esame di Reti')
    print('A. Conti, A. Mastrilli, U. Baroncini')
    open_socket()
    
    have_to_receive_first_connection = True
    while len(client_sockets) > 0 or have_to_receive_first_connection:
        if (len(client_sockets) > 0):
            have_to_receive_first_connection = False
        sleep(0.1)
    
    print('Everyone left! Bye!')


def close_connection(id):
    client_sockets[id]['socket'].close()
    client_sockets.pop(id)


start_server()