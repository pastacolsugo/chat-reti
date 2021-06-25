# Progetto Reti traccia 3

### Per eseguire

Impostare il path corretto per il file `config.json`, in base alla propria macchina. La variabile contenente il path si trova all'inizio del file `server.py`.

```python
# Set the correct path for your machine!
CONFIG_FILE_PATH = '/Users/sugo/git/chat-reti/src/config.json'
```

Avere installato `python 3.9.5` e `tk`, avere la porta `8080` libera.
Eseguire una istanza di `server.py`, e tante istanze di `client.py` tanti quanti sono i giocatori che si vogliono impersonare.
Il server ha solamente l'interfaccia testuale da riga di comando, in quanto non richiede interazione da parte dell'utente, ma fornisce solo qualche messaggio di log durante lo svolgimento del gioco.

Ogni istanza di client aprirà una finestra tk tramite la quale il giocatore interagirà con il gioco.

Sarà sufficiente inserire il nome per ogni giocatore, collegarsi al server e premere `Start Game!` da uno dei client e giocare.

### Per esaminare il traffico di rete

Per esaminare il traffico di rete abbiamo usato Wireshark, catturando sull'interfaccia di loopback e usando il filtro `tcp.port == 8080 and tcp.flags.push == 1` per visualizzare solo i messaggi da e per il server, inviati dalle applicazioni.