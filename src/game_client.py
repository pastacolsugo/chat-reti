# Laboratorio di Programmazione di Reti - Universit di Bologna - Campus di Cesena
# Giovanni Pau - Andrea Piroddi

import tkinter as tk
import json
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading

player_name = ""
player_role = ""
score = 0
game_started = False

# Socket client
client_socket = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8000
 
window_main = tk.Tk()
window_main.title("Game Client")

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
answer_buttons = []
for i in range(4):
    answer_buttons.append(tk.Button(answer_buttons_frame, text=f'answer_button_{i}'))
    answer_buttons[i].pack(side = tk.LEFT)

choice_buttons_frame = tk.Frame(window_main)
choice_buttons = []
for i in range(3):
    choice_buttons.append(tk.Button(choice_buttons_frame, text=f'choice_button_{i}'))
    choice_buttons[i].pack(side = tk.LEFT)

start_button_frame = tk.Frame(window_main)
start_button = tk.Button(start_button_frame, text="Start game!", command = lambda : send_start_game(), state=tk.DISABLED)
start_button.pack(side = tk.TOP)
start_button_frame.pack(side = tk.BOTTOM)

def send_start_game():
    global game_started
    msg = {
        'start_game' : True
    }
    client_socket.send(json.dumps(msg).encode())
    start_button.config(state=tk.DISABLED)
    game_started = True

def answer(ans_number):
    print(f'Answered {ans_number}')

def send_answer(ans_number: int):
    msg = {
        'answer' : ans_number
    }
    client_socket.send(json.dumps(msg).encode())

def send_choice(choice: str):
    msg = {
        'choice' : choice
    }
    client_socket.send(json.dumps(msg).encode())
    hide_choice_buttons()


def hide_answer_buttons():
    answer_buttons_frame.pack_forget()

def show_answer_buttons():
    answer_buttons_frame.pack(side = tk.TOP)

def hide_choice_buttons():
    choice_buttons_frame.pack_forget()

def show_choice_buttons():
    choice_buttons_frame.pack(side = tk.TOP)

def update_role(role):
    role_label.config(text = f'Role : {role}')

def connect():
    global player_name
    if len(name_text_field.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your name first <e.g. Giovanni>")
    else:
        player_name = name_text_field.get()
        connect_to_server()


# def choice(arg):
#     global your_choice, client, game_round
#     your_choice = arg
#     lbl_your_choice["text"] = "Your choice: " + your_choice

#     if client:
#         client.send(("Game_Round"+str(game_round)+your_choice).encode())
#         enable_disable_buttons("disable")


def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST_ADDR, HOST_PORT))

        # Listen to socket on a separate thread
        threading._start_new_thread(handle_server_communication, ())
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")
        print(e)


def handle_server_communication():
    global game_started

    # Disable connection widgets
    connect_button.config(state=tk.DISABLED)
    name_text_field.config(state=tk.DISABLED)
    name_label.config(state=tk.DISABLED)

    # Send player name to server
    msg = {
        "player_name" : player_name
    }
    client_socket.send(json.dumps(msg).encode()) 

    # Wait for assigned role from server
    msg = client_socket.recv(2048).decode()
    if not msg:
        # TODO: exit gracefully
        return

    player_role = json.loads(msg)['player_role']
    update_role(player_role)
    print(player_role)
    
    # Enable game start button
    start_button.config(state=tk.ACTIVE)

    # Wait for the player to press the start button
    # or the server saying the game has started
    while not game_started:
        try:
            msg = client_socket.recv(1024, socket.MSG_DONTWAIT).decode()
            if not msg:
                # TODO: exit gracefully
                return
            if json.loads(msg)['game_started']:
                game_started = True
        except Exception as e:
            pass

    print('waiting for option')
    # Receive option
    try:
        msg = client_socket.recv(8192).decode()
    except Exception as e:
        print("oops")
        print(e)
        return

    print(msg)
    if not msg:
        # TODO: exit gracefully
        return
    option = json.loads(msg)
    print(option)

    # Display option text and buttons
    question_label.config(text = option['option_question'])
    for btn, opt in zip(choice_buttons, option['option_answers']):
        choice_text = opt['option']
        btn.config(text = choice_text, command = lambda choice=choice_text: send_choice(choice))
    show_choice_buttons()
    
    # Wait either for the first question or the dropped connection (kicked)
    msg = client_socket.recv(4096).decode()
    if not msg:
        # TODO: exit gracefully
        return
    

    client_socket.close()


window_main.mainloop()