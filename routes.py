from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
import threading

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/my_team')
def my_team():
    return render_template('my_team.html')

@app.route('/add_player', methods=['POST'])
def add_player():
    player_name = request.form['player_name']
    session['player_name'] = player_name
    return redirect(url_for('play'))

@app.route('/remove_player', methods=['POST'])
def remove_player():
    session.pop('player_name', None)
    return redirect(url_for('play'))

@app.route('/pokemon/<int:pokemon_id>')
def pokemon(pokemon_id):

    # Récupère les données du Pokémon
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()

    return pokemon

@app.route('/add_pokemon_to_team/<int:pokemon_id>', methods=['POST'])
def add_pokemon_to_team(pokemon_id):
    # Vérifie que le joueur a un nom défini
    if 'player_name' not in session:
        return redirect(url_for('play'))

    # Initialise la structure de données si nécessaire
    if not isinstance(session['player_name'], dict):
        session['player_name'] = {'name': session['player_name'], 'team': []}
    elif 'team' not in session['player_name']:
        session['player_name']['team'] = []

    # Ajoute le Pokémon à l'équipe
    session['player_name']['team'].append(pokemon_id)

    return f"Pokémon {pokemon_id} ajouté à l'équipe de {session['player_name']['name']}."

def fetch_pokemon_data(pokemon_url, results):
    """
    Fonction exécutée par un thread pour récupérer les données d'un Pokémon.
    """
    try:
        new_pokemon = requests.get(pokemon_url).json()
        pokemon_data = {
            'name': new_pokemon['name'],
            'image': new_pokemon['sprites']['front_default'],
            'id': new_pokemon['id']
        }
        results.append(pokemon_data)
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {pokemon_url}: {e}")


@socketio.on('get_pokemons')
def handle_get_pokemons():
    # Récupère les 151 Pokémon
    pokedex = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')
    pokemon_urls = [pokemon['url'] for pokemon in pokedex.json()['results']]
    
    results = []
    threads = []

    # Divise les URLs en 4 groupes pour 4 threads
    num_threads = 5
    chunk_size = len(pokemon_urls) // num_threads

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(pokemon_urls)
        thread = threading.Thread(target=lambda: [fetch_pokemon_data(url, results) for url in pokemon_urls[start:end]])
        threads.append(thread)
        thread.start()

    # Attends que tous les threads se terminent
    for thread in threads:
        thread.join()

    # Envoie les données récupérées au client
    for pokemon_data in results:
        emit('pokemon_data', pokemon_data)