from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon/<int:pokemon_id>')
def pokemon(pokemon_id):

    # Récupère les données du Pokémon
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()

    return pokemon


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