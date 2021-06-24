###### Programmazione di Reti - Università di Bologna - A.A. 2020-2021

###### Baroncini Ugo ugo.baroncini@studio.unibo.it 0000842092

###### Conti Alice alice.conti7@studio.unibo.it 0000925054

###### Mastrilli Alice alice.mastrilli@studio.unibo.it 0000925517


# Traccia 3 - Chat Game

# Introduzione
Il progetto è stato realizzato utilizzando il linguaggio Python creando una connessione client-server sfruttando il protocollo TCP-IP.
Il gioco realizzato prevede, dopo un iniziale login da parte del giocatore (client), una domanda iniziale con 3 possibili risposte: due di queste sono corrette, l'altra è errata. Scegliendo la risposta scorretta, termina automaticamente la connessione del giocatore che ha sbagliato ed esce dal gioco.
Se invece la fase iniziale viene superata, il gioco inizierà: si susseguiranno una serie di domande con cui si acquisiscono o perdono punti a seconda se la risposta data è corretta o errata.
Il giocatore che arriva per primo ai 5 punti decreta la fine del gioco e viene mostrata la classifica con i relativi punteggi dei giocatori e successivamente tutti perdono la connessione.

 # Descrizione
 Per la realizzazione dell'applicazione sono stati realizzati due diversi programmi che rispettivamente gestiscono i client e il server del gioco:
 - client.py
 - server.py
 
 I programmi sono entrambi eseguibili con python3 (nello specifico versione 3.9.5).
 In aggiunta a questi, è presente un file .json `config.json` in cui sono salvate le domande, le risposte e alcuni parametri di configurazione.
 Questo file servirà per la generazione di domande da porre all'utente, scelte casualmente tra quelle disponibili.
 
 ## Strutture dati
 Le principali strutture dati utilizzate sono dizionari (struttura dati che memorizza coppie chiavi-valori) e le liste. 
 Le liste sono state utilizzate per l'implementazione dell'interfaccia grafica.
 La scelta del dizionario è stata basata per la serializzazione con .json molto comoda che ha semplificato la comunicazione. 
 
 ## Server
Come si può osservare nel file `server.py` tra i parametri più rilevanti da considerare ci sono gli indirizzi IP e la porta del server (utili quando verrà stabilita la connessione).
Inoltre `client_sockets` è un dizionario dei socket dei client, che aumenta ogni volta che un client si collega, `server_socket` è la porta su cui il server si mette in ascolto e viene attivata in `open_socket()`, chiamata una volta avviato il server. 
 ```python
def open_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST_ADDR, HOST_PORT))
    server_socket.listen(5) # allowed connection attempts

    threading._start_new_thread(accept_new_clients, (server_socket,))
 ```
 Inizialemente il socket del server viene associato all'indirizzo `HOST_ADDR` e alla porta `HOST_PORT`, dichiarati precedentemente.
 Successivamente il server si mette in attesa di clients e, ogni volta che un client si collega, viene creato un nuovo thread e chiamata la funzione `accept_new_clients()`.
 ```python
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
 ```
 Richiamando la funzione `get_next_connection_id()`, viene assegnato un ID ad ogni connessione, che verrà passato come argomento nella funzione `handle_player_connection()`.
 
 La gestione del player consiste nel ricevere dal client il nome di login e successivamente assegnargli un ruolo scelto casualmente dal file .json.
 A questo punto si mette in attesa che un client avvii il gioco. 
 ```python
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
 ```
 
 Questo avviene tramite dei check che controllano 10 volte ogni secondo se un client ha dato il via alla partita.
 Una volta che il primo giocatore ha fatto iniziare la partita, il gioco comincia e viene mostrata la prima domanda preliminare, anche questa scelta casualmente dalla sezione `option` del file .json.
 Se la risposta scelta è sbagliata il giocatore termina la connessione
 ```python
 if not msg:
        return # TODO: handle exit
    player_choice = json.loads(msg)['choice']
 ```
 I client che invece hanno scelto la risposta giusta riceveranno la prima domanda.
 ```python
 # while (number of questions < X):
    while score < GAME_CONFIG['winning_score'] and not is_game_over:
        # Serve question
        question = random.choice(GAME_CONFIG['questions'])
        player_socket.send(json.dumps(question).encode())

        # Wait for answer
        msg = player_socket.recv(4096).decode()
        if not msg:
            return

        # expected object
        # {'answer' : '3'}
        player_answer = json.loads(msg)['answer']

        print("player_answer")
        print(player_answer)
        
        # Check answer and assign points
        if player_answer == question['correct_answer']:
            score += 1
        else:
            score -= 1 
        
        # Send new score to client
        score_update = {'score' : score}
        player_socket.send(json.dumps(score_update).encode())
 ```
 A ogni scelta del giocatore il server valuta la risposta ricevuta, aggiorna di conseguenza il punteggio e manda ai client la domanda successiva. 
 Questa sequenza si ripete finchè un player non arriva a 5 punti.
 A quel punto il gioco termina per tutti i client e viene stilata una classifica che il server manda ad ognuno di loro.
 ```python
 
    # Send ranking
    player_socket.send(serialized_ranking.encode())
```

Come ultimo passaggio viene chiusa la connessione.

## Client
Una volta avviato il client viene subito richiesto il login e l'avvio della connessione. Queste funzionalità vengono gestite tramite le funzioni `connect()` e `connect_to_server()`. In quest'ultima viene creato un nuovo thread su cui viene stabilita la connessione con il server (dal momento che il thread principale sta venendo utilizzato per l'interfaccia grafica.
Come in `server`, la funzione `handle_server_communication()` gestisce la comunicazione tra server e client.
Dopo aver inviato al server il proprio username di login, riceve il ruolo e attende che un altro giocatore avvii il gioco. 
A questo punto riceverà la domanda preliminare che verrà mostrata a video insieme alle possibili risposte; una volta scelta verrà comunicata al server che, se corretta permette di continuare il gioco, altrimenti termina la connessione.

Ciascun client riceverà i messaggi dal server (questions o ranking) e una volta ricevuta la classifica viene chiusa la connessione con il server.

![alt text](https://github.com/pastacolsugo/chat-reti/blob/main/Diagram.png)


## Thread attivi
Come precedentemente spiegato, server e client lavorano su più thread: 
- il server ha un proprio thread sempre attivo dove rimane in attesa di nuove comunicazioni e tanti altri quanti sono i clients collegati
- il client ha un thread che utilizza per l'interfaccia grafica e tanti altri quanti sono i players
 
 
 
 
 
 

