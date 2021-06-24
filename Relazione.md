

# Introduzione
Il progetto è stato realizzato utilizzando il linguaggio Python creando una connessione clinet-server sfruttando il protocollo TCP-IP.
Il gioco realizzato prevede, dopo un iniziale login da parte del giocatore (client), una domanda iniziale con 3 possibili risposte: due di queste sono corrette, l'altra è errata. Scegliendo la risposta scorretta, termina automaticamente la connessione e si esce dal gioco.
Se invece la fase iniziale viene superata, il gioco inizierà: si susseguiranno una serie di domande con cui si acquisiscono o perdono punti a seconda se la risposta data è corretta o errata.
Il giocatore che arriva per primo ai 5 punti, decreta la fine del gioco, viene mostrata la classifica con i relativi punteggi dei giocatori e successivamente tutti perdono la connessione.

 # Descrizione
 Per la realizzazione dell'applicazione sono stati realizzati due diversi programmi che rispettivamente gestiscono i client e il server del gioco:
 - client.py
 - server.py
 
 I programmi sono entrambi eseguibili con python3 (nello specifico versione 3.9.5).
 In aggiunta a questi, è presente un file .json `config.json` in cui sono salvate le domande, le risposte e alcuni parametri di configurazione.
 Questo file servirà per la generazione di domande da porre all'utente, scelte casualmente tra quelle disponibili.
 
 ## Server
 Come si può osservare nel file `server.py` tra i parametri più rilevanti da considerare ci sono gli indirizzi IP e la porta del server (utili quando verrà stabilita la connessione) e la lista dei client connessi (client_socket).
 Inoltre `client_sockets` è la lista dei socket dei client, che aumenta ogni volta che un client si collega.
 Mentre `server_socket` è la porta su cui il server si mette in ascolto, che viene attivata in `open_socket`.
 Una volta avviato il server viene subito chiamata la funzione `open_socket` 
 ```python
def open_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST_ADDR, HOST_PORT))
    server_socket.listen(5) # allowed connection attempts

    threading._start_new_thread(accept_new_clients, (server_socket,))
 ```
 Inizialemente il socket del server viene associato all'indirizzo `HOST_ADDR` e alla porta `HOST_PORT`, dichiarati precedentemente.
 Successivamente si mette in attesa di client, e ogni volta che un client si collega viene creato un nuovo thread e chiama la funzione `accept_new_clients`.
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
 Richiamando la funzione `get_next_connection_id`, viene dato un ID ad ogni connessione, che verrà passato come argomento nella funzione `handle_player_connection`.
 
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
 Una volta che il primo giocatore ha fatto iniziare la partita, il gioco comincia e viene mostrata la prima domanda "preliminare", anche questa scelta casualmente dalla sezione `option` del gile .json.
 Se la risposta scelta è sbagliata il giocatore termina la connessione
 ```python
 if not msg:
        return # TODO: handle exit
    player_choice = json.loads(msg)['choice']
 ```
 I client che invece hanno scelto la risposta giusta riceveranno la prima domanda.
 A ogni scelta del giocatore il server valuta la risposta ricevuta, aggiorna di conseguenza il punteggio e manda ai client la domanda successiva. 
 Questa sequenza si ripete finchè un player non arriva a 5 punti.
 A quel punto il gioco termina per tutti i client e viene stilata una classifica che il server manda ad ogni client.
 ```python
 
    # Send ranking
    player_socket.send(serialized_ranking.encode())
```

Come ultimo passaggio viene chiusa la connessione.
 
 
 
 
 
 
 

