import flask
from flask import jsonify, request, render_template
import sqlite3
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return "<h1>Biblioteca online</h1>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    database = sqlite3.connect('db/books.db')   #connessione al database
    c = database.cursor()
    c.execute("SELECT * FROM books ORDER BY year_published")    #esegue la query
    all_books = c.fetchall()    #recupera in una lista di liste tutto quello selezionato dalla query
    return jsonify(all_books)   #restituisce i risultati in un file json

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    database = sqlite3.connect('db/books.db')
    c = database.cursor()
    print(request.args) #lettura da url dell'id passato
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Errore: Non è stato immesso alcun id"

    c.execute(f"SELECT * FROM books WHERE id LIKE '{id}'")  #ricerca nel database del libro per id
    book = c.fetchall()

    return jsonify(book)

app.run()