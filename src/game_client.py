# Laboratorio di Programmazione di Reti - Universit di Bologna - Campus di Cesena
# Giovanni Pau - Andrea Piroddi

import tkinter as tk
import json
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading

from server import start_server

# FINESTRA DI GIOCO PRINCIPALE
window_main = tk.Tk()
window_main.title("Game Client")
player_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0

# client di rete
client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8000

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST_ADDR, HOST_PORT))
# client.send("ali".encode())

# load json file: his content is in the dictionary dic
# data = client.recv(4096)
# dic = json.loads(data.decode())
# dictionary of options
# option_dictionary = dic['options']

player_name_frame = tk.Frame(window_main)
name_label = tk.Label(player_name_frame, text = "Name:")
name_label.pack(side = tk.LEFT)
name_text_field = tk.Entry(player_name_frame)
name_text_field.pack(side = tk.LEFT)
connect_button = tk.Button(player_name_frame, text="Connect", command=lambda : connect())
connect_button.pack(side = tk.LEFT)
player_name_frame.pack(side = tk.TOP)

score_and_role_frame = tk.Frame(window_main)
score_and_role_frame.pack(side = tk.TOP)

score_display_frame = tk.Frame(score_and_role_frame)
point_label = tk.Label(score_display_frame, text = "Score: 0")
point_label.pack(side = tk.RIGHT)
score_display_frame.pack(side = tk.RIGHT)

role_display_frame = tk.Frame(score_and_role_frame)
role_label = tk.Label(role_display_frame, text = "Role : -")
role_label.pack(side = tk.LEFT)
role_display_frame.pack(side = tk.LEFT)

question_display_frame = tk.Frame(window_main)
question_label = tk.Label(question_display_frame, text = "Ready for some questions?")
question_label.pack(side = tk.TOP)
question_display_frame.pack(side = tk.TOP)

answer_buttons_frame = tk.Frame(window_main)
answer_0_button = tk.Button(answer_buttons_frame, text='Answer 0', command = lambda : answer(0))
answer_1_button = tk.Button(answer_buttons_frame, text='Answer 1', command = lambda : answer(1))
answer_2_button = tk.Button(answer_buttons_frame, text='Answer 2', command = lambda : answer(2))
answer_3_button = tk.Button(answer_buttons_frame, text='Answer 3', command = lambda : answer(3))
answer_0_button.pack(side = tk.LEFT)
answer_1_button.pack(side = tk.LEFT)
answer_2_button.pack(side = tk.LEFT)
answer_3_button.pack(side = tk.LEFT)

choice_buttons_frame = tk.Frame(window_main)
choice_0_button = tk.Button(choice_buttons_frame, text = "Choice 0", command = lambda : choose(0))
choice_1_button = tk.Button(choice_buttons_frame, text = "Choice 1", command = lambda : choose(1))
choice_2_button = tk.Button(choice_buttons_frame, text = "Choice 2", command = lambda : choose(2))
choice_0_button.pack(side = tk.LEFT)
choice_1_button.pack(side = tk.LEFT)
choice_2_button.pack(side = tk.LEFT)

start_button_frame = tk.Frame(window_main)
start_button = tk.Button(start_button_frame, text="Start game!", command = lambda : send_start_game(), state=tk.DISABLED)
start_button.pack(side = tk.TOP)
start_button_frame.pack(side = tk.BOTTOM)

def send_start_game():
    pass

def answer(ans_number):
    print(f'Answered {ans_number}')

def choose(choice_number):
    print(f'Chosen {choice_number}')

def hide_answer_buttons():
    answer_buttons_frame.pack_forget()

def show_answer_buttons():
    answer_buttons_frame.pack(side = tk.TOP)

def hide_choice_buttons():
    choice_buttons_frame.pack_forget()

def show_choice_buttons():
    choice_buttons_frame.pack(side = tk.TOP)

def connect():
    global player_name
    if len(name_text_field.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        player_name = name_text_field.get()
        connect_to_server()


def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "Your choice: " + your_choice

    if client:
        client.send(("Game_Round"+str(game_round)+your_choice).encode())
        enable_disable_buttons("disable")


def connect_to_server():
    global client_socket, HOST_PORT, HOST_ADDR
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST_ADDR, HOST_PORT))
        client_socket.send(player_name.encode()) # Invia il nome al server dopo la connessione

        # disable widgets
        connect_button.config(state=tk.DISABLED)
        name_text_field.config(state=tk.DISABLED)
        name_label.config(state=tk.DISABLED)
        start_button.config(state=tk.ACTIVE)

        # avvia un thread per continuare a ricevere messaggi dal server
        # non bloccare il thread principale :)
        threading._start_new_thread(receive_message_from_server, ())
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")
        print(e)


def receive_message_from_server():
    global client_socket, player_name

    while True:
        from_server = client_socket.recv(4096).decode()

        if not from_server:
            break

        if from_server.startswith("welcome".encode()):
            if from_server == "welcome1":
                lbl_welcome["text"] = "Server says: Welcome " + player_name + "! Waiting for player 2"
            elif from_server == "welcome2":
                lbl_welcome["text"] = "Server says: Welcome " + player_name + "! Game will start soon"
            lbl_line_server.pack()

        elif from_server.startswith("opponent_name$".encode()):
            opponent_name = from_server.replace("opponent_name$".encode(), "".encode())
            lbl_opponent_name["text"] = "Opponent: " + opponent_name.decode()
            top_frame.pack()
            middle_frame.pack()

            # sappiamo che due utenti sono connessi, quindi il gioco  pronto per iniziare
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$opponent_choice".encode()):
            # ottieni la scelta dell'avversario dal server
            opponent_choice = from_server.replace("$opponent_choice".encode(), "".encode())

            # capire chi vince in questo round
            who_wins = game_logic(your_choice, opponent_choice.decode())
            round_result = " "
            if who_wins == "you":
                your_score = your_score + 1
                round_result = "WIN"
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            # Aggiorna GUI
            lbl_opponent_choice["text"] = "Opponent choice: " + opponent_choice.decode()
            lbl_result["text"] = "Result: " + round_result

            # e questo l'ultimo round ad es. Round 5?
            if game_round == TOTAL_NO_OF_ROUNDS:
                # calcola il risultato finale
                final_result = ""
                color = ""

                if your_score > opponent_score:
                    final_result = "(You Won!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                lbl_final_result["text"] = "FINAL RESULT: " + str(your_score) + " - " + str(opponent_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0

            # Avvia il timer
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()


window_main.mainloop()