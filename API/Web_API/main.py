import flask
from flask import jsonify, request
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return "<h1>Biblioteca online</h1>"

@app.route('/api/v1/resources/book/all', methods=['GET'])   #tutti i libri
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])  #ricerca per id
def api_id():
    if 'id' in request.args:
        id = int(request.args['id']) #prende l'id inserito nell'URL
    else:
        return "Errore: Non è stato immesso alcun id"

    risultati = []
    for book in books:
        if book['id'] == id:
            risultati.append(book)  #aggiunge a una lista i libri con gli id passati
    return jsonify(risultati)

books = [       #dizionario
    {
        'id': 0,
        'title': 'Il nome della Rosa',
        'author': 'Umberto Eco',
        'year_published': '1980'
    },
    {
        'id': 1,
        'title': 'Il problema dei tre copri',
        'author': 'Liu Cixin',
        'year_published': '2008'
    },
    {
        'id': 2,
        'title': 'Fondazione',
        'author': 'Isaac Asimov',
        'year_published': '1951'
    },
]
app.run()