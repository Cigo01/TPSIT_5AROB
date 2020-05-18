import sqlite3
import flask
from flask import jsonify,request
from datetime import datetime
'''
Server Cigottero Marco 5AROB
'''
app = flask.Flask(__name__)

@app.route('/api/v1/user_list', methods=['GET'])
def api_home():
    try:
        sqliteConn = sqlite3.connect('chatDB.db')
        cursor = sqliteConn.cursor()

        cursor.execute("SELECT * FROM utenti")  #ricerco tutti gli utenti
        user = cursor.fetchall()

    except sqlite3.Error as error:
        print("Error: " + error)

    finally:
        if (sqliteConn):
            print('chiusura connessione DB')
            sqliteConn.close()

    return jsonify(user)    #ritorno gli utenti in file json

@app.route('/api/v1/receive', methods=['GET'])
def ricevere():
    if 'id_dest' in request.args:
        dest = int(request.args['id_dest']) #salvataggio id_dest
        try:
            sqliteConn = sqlite3.connect('chatDB.db')#connessione al database
            cursor = sqliteConn.cursor()

            cursor.execute(f"SELECT sender_id,text,receiver_id,timestamp "
                           f"FROM messaggi "
                           f"WHERE received=0  AND receiver_id = {dest}")

            if len(cursor.fetchall()) != 0:
                for i in cursor.fetchall(): #scorro il db
                    cursor.execute(f'''UPDATE messaggi 
                                        SET received = 1 
                                        WHERE messaggi.timestamp < datetime('now') and messaggi.receiver_id = {i[2]}''')
                    sqliteConn.commit()

        except sqlite3.Error as error:
            print(error)

        finally:
            if (sqliteConn):
                print('chiusura connessione DB')
                sqliteConn.close()
    else:
        return "invalid user id"
    return jsonify(cursor.fetchall()) #ritorno in file json

@app.route('/api/v1/send', methods=["GET"])
def inviare():
    date = datetime.now()
    time = date.strftime("%H:%M:%S")

    if 'id_dest' in request.args and 'text' in request.args and 'id_mitt' in request.args:
        dest = int(request.args['id_dest']) #salvo i parametri passati
        text = request.args['text']
        mitt = int(request.args['id_mitt'])
    else:
        return("errore: argomenti mancanti ")

    try:
        sqliteConn = sqlite3.connect('chatDB.db')
        cursor = sqliteConn.cursor()

        cursor.execute(f"SELECT user_id from utenti WHERE user_id = {mitt} or user_id = {dest} ")
        users = cursor.fetchall()

        if len(users) > 1: #controllo se c'è l'utente
            cursor.execute(f"INSERT INTO messaggi(text,timestamp,length,received,receiver_id,sender_id) VALUES ('{text}','{time}',{len(text)},{False},{dest},{mitt})")
            sqliteConn.commit()
        else:
            return "utenti non registrati nel database"

    except sqlite3.Error as error:
        print("Error: " + error)

    finally:
        if (sqliteConn):
            print('chiusura connessione DB')
            sqliteConn.close()

    return "Messaggio inviato"

if __name__== "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

