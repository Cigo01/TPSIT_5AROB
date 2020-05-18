import sqlite3
from threading import Thread
import flask
from flask import jsonify, request
from datetime import datetime
import threading
#import requests
import time
'''
Client Cigottero Marco 5AROB
'''
class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)   #dichiarazione attributi del thread
        self.id = myId
        self.ip = ip
        self.url_conn="http://" + ip + "/api/v1/receive"
    def run(self):
        while True:
            time.sleep(15)
            params = {'id_dest': self.id}
            URL=self.url_conn
            r = requests.get(url=URL, params=params)

            try:
                sqliteConn = sqlite3.connect('db_client_cigottero.db')
                cursor = sqliteConn.cursor()

                if len(r.json()) != 0:
                    for i in r.json():
                        cursor.execute(
                            f'''
                                INSERT INTO Mess_R(Text, Id_Mitt) 
                                VALUES ("{d[3]}", {d[0]});''') #inserisco il messaggio nel DB
                        sqliteConn.commit()

            except sqlite3.Error() as err:
                print('Error: ' + err)
            finally:
                if (sqliteConn):
                    sqliteConn.close()

def Messaggi_ricevuti(): #Stampo i record salvati dal thread nel DB'''
    try:
        sqliteConn = sqlite3.connect(db_client_cigottero.db)   #apro connessione
        cursor = sqliteConn.cursor()                            # istanzio cursore

        cursor.execute(f"SELECT Mess_R.text, utenti.nick FROM Mess_R, utenti WHERE utenti.user_id = Mess_R.Id_Mitt;")
        for d in data:      #scorro per i risultati
            print(f"Messaggio ricevuto da: {d[1]} - Testo: {d[0]}")

        sqliteConn.commit()

    except sqlite3.Error as error:
        print("Error: " + error)

    finally:
        if (sqliteConn):
            sqliteConn.close()  #chiudo la conn

def Manda_messaggi():
    id_dest = int(input("\nInserisci il numero di registro del destinatario"))
    text = input("\nInserisci testo del messaggio\n")

    params = {'id_dest': id_dest, 'text': text, 'id_mitt': myId}
    text = text.replace(" ", "+")
    URL = "http://" + ip + "/api/v1/send"

    r = requests.get(url=URL, params=params)
    if r.status_code == 200:
        print("messaggio inviato")
    else:
        print("non sono riuscito ad inviare il messaggio")

    return

def Cambia_Stato(): #funzione per sbloccare o bloccare gli utenti
    try:
        sqliteConn = sqlite3.connect(db_client_cigottero.db)
        cursor = sqliteConn.cursor()

        user = input("Seleziona l'utente di cui vuoi cambiare lo stato\n")
        cursor.execute(f"SELECT bloccato FROM utenti WHERE nick = '{user}';")
        data = cursor.fetchall()    #carico i risultati in questa lista
        cursor.execute(f'''UPDATE utenti 
                                    SET bloccato = {(data[0][0]+1)%2}  
                                    WHERE nick = "{user}"''')   #cambio lo stato se è 1(1+1=2 2%2=0) se è a 0(0+1=1 1%2=1)

        sqliteConn.commit() #salvo lo stato

    except sqlite3.Error as error:
        print("Error: " + error)

    finally:
        if (sqliteConn):
            sqliteConn.close()
def Lista_utenti():
    URL = "http://" + ip + "/api/v1/user_list"
    r = requests.get(url=URL)
    data = r.json()
    for i in data:
        print(i[0], " ", i[1], " ", i[2])

def Menu():
    print("0 - Esci")
    print("1 - Rubrica")
    print("2 - Messaggi ricevuti")
    print("3 - Invia")
    print("4 - Blocca/Sblocca")

def main(idReg, avThread):

    while True:
        Menu()
        azione = int(input("->"))
        if azione == 0:
            avThread.join()
            break
        elif azione == 1:
            Lista_utenti()

        elif azione == 2:
            Messaggi_ricevuti()

        elif azione == 3:
            Manda_messaggi()

        elif azione == 4:
            Cambia_Stato()

        else:
            pass

if __name__ == "__main__":
    myId = int(input("inserisci il tuo numero di registro:\n "))
    ip = input("\nInserisci ip e porta del server \n")

    avThread = ClientThread()
    avThread.start()
    main(myId, avThread)