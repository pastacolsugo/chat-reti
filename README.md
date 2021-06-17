# chat-reti

Traccia 3: CHATGAME
Sfruttando il principio della CHAT vista a lezione implementate
un’architettura client-server per il supporto di un Multiplayer
Playing Game testuale.
I giocatori che accedono alla stanza sono accolti dal Master
(server) che assegna loro un ruolo e propone loro un menu con
tre opzioni, due delle quali celano una domanda mentre la
terza è l’opzione trabocchetto. Se sceglie l’opzione
trabocchetto viene eliminato dal gioco e quindi esce dalla chat.
Se seleziona invece una delle domande e risponde
correttamente al quesito acquisisce un punto, in caso contrario
perde un punto.
Il gioco ha una durata temporale finita; il giocatore che al
termine del tempo ha acquisito più punti è il vincitore.

## Link Utili

- [Repo Github](https://github.com/pastacolsugo/chat-reti)
- [Corso di reti su Virtuale](https://virtuale.unibo.it/course/view.php?id=19303)
- [Tracce dei progetti](https://virtuale.unibo.it/pluginfile.php/828762/mod_resource/content/1/tracce%20Progetti%20di%20fine%20corso%202020_2021.pdf)
- [Slide laboratorio #12](https://virtuale.unibo.it/pluginfile.php/839201/mod_resource/content/1/Programmazione%20di%20Reti%20%2312.pdf)
- [Codide laboratorio #12](https://virtuale.unibo.it/mod/resource/view.php?id=582946)
- [Esempio vecchia traccia #3](https://virtuale.unibo.it/pluginfile.php/827640/mod_folder/content/0/Soluzione%20Traccia%203.zip?forcedownload=1)
- [UML diagram](https://drive.google.com/file/d/1XpP_2LWAPwCf7kCqTwBBZNEAGpzvGudY/view?usp=sharing)


## Requirements:

- multiplayer
- game-master
- ruolo
- tre opzioni
	* opzione trabocchetto
	* due opzioni safe
- domande
	* risposta giusta +1 
	* risposta sbagliata -1 
- limite di tempo
- vincitori/perdenti
- possibilita' di fare piu' round 

## Criteri di valutazione

* Eseguibilità del codice e rispetto dei requirements indicati nelle tracce
* Presenza di Commenti esplicativi nel codice
* Relazione dettagliata con riferimenti specifici all’utilizzo dei socket
* Una descrizione generale delle scelte di progetto effettuate
* Una descrizione delle strutture dati utilizzate
* Uno schema generale dei threads attivati sia nei server che nel client
* L’organizzazione e la chiarezza dell’esposizione della relazione
* L’utilizzo di metodologie di documentazione del software quali diagrammi UML (delle classi, di sequenza,...) sara' considerato positivamente ai fini della valutazione del progetto.

## User story

**1]** Con il server attivo, lancio il client sulla mia macchina e si apre una finestra con un'interfaccia di login. Inserisco un nome utente ed entro nella lobby, dove trovo una lista dei giocatori connessi aggiornata in tempo reale e due pulsanti, uno per scollegarmi e uno per iniziare il round. Premo il pulsante per iniziare il round e la finestra cambia, mostrando un timer che cala ogni secondo (tempo del round) e tre opzioni. `{1}` Scelgo una delle tre e mi disconnette dal gioco. Mi ricollego e vengo messo in una lobby in attesa che la partita in corso finisca. Finche' l'altra partita e' ancora in corso non ne posso iniziare una nuova e tutti i giocatori che si connettono in questo momento vengono aggiunti alla lobby di attesa.
Quando la partita precedente finisce, sono gia' in lobby e posso giocare di nuovo.

**2]** (come prima fino a `{1}`) Scelgo una delle due opzioni "buone". L'interfaccia cambia e mi viene mostrata una domanda con 4 possibili risposte. Scelgo la mia risposta e mi viene aggiunto un punto se era corretta oppure decurtato un punto se era sbagliata. Si susseguono tante domande fino allo scadere del tempo. 
Terminato il tempo a disposizione l'interfaccia cambia e si presenta una classifica dei giocatori in base al punteggio raggiunto. Vince chi ha piu' punti. Sotto la classifica ci sono due pulsanti: uno per disconnettersi e uno per tornare in lobby.

**3]** Sono admin del gioco, lancio il server e mi appare una finestra con due pulsanti: uno per attivare il server e uno per fermarlo. Sotto i due pulsanti vedo un campo di testo contenente l'IP e la porta del server. Sotto l'IP e la porta vedo un ulteriore campo di testo con un log di quello che succede.

