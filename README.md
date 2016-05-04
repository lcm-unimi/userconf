# userconf
Suit for ldap users management

userconf e' uno script in Python per gestire gli utenti in un database 
LDAP. Il modulo su cui si basa e' npyscreen, scelto rispetto
curses e urwin in quanto di livello piu' alto e con un codice sorgente
semplice e accessibile che unitamente alla ricca documentazione permette
di prendere dimistichezza con le funzioni in poco tempo.

Attualmente userGUI non implementa nessuna funzione di userconf ma e'
solo una GUI (che gira in console) parzialmente funzionante.

Lo script userconf.py importa userGUI che definisce le funzioni per 
disegnare l'interfaccia grafica, mentre lcmldap si occupa di gestire la 
connessione e le funzioni legate al database ldap.


Richiede npyscreen >= 4.4.0
