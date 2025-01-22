from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
import threading
import random
import enum

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    if 'player_name' not in session: 
        session['player_name'] = {'name': 'Joueur', 'team': []}
    return render_template('play.html')

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
    """
    Récupère les données d'un Pokémon.

    Args:
        pokemon_id (int): L'identifiant du Pokémon à récupérer.
    
    Returns:
        pokemon (dict): Un dictionnaire contenant les informations sur le Pokémon.
    """

    # Récupère les données du Pokémon
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()

    return pokemon

@app.route('/get_pokemon_team', methods=['GET'])
def get_pokemon_team():
    """
    Récupère l'équipe du joueur.

    Returns:
        team (dict): Un dictionnaire contenant les informations sur l'équipe du joueur.
    """
    if 'player_name' in session:
        print(session['player_name'])
        return session['player_name']['team']
    return {}

@app.route('/add_pokemon_to_team/<int:pokemon_id>', methods=['POST'])
def add_pokemon_to_team(pokemon_id):
    """
    Ajoute un Pokémon à l'équipe du joueur.

    Args:
        pokemon_id (int): L'identifiant du Pokémon à ajouter.

    Returns:
        response (dict): Un dictionnaire contenant le code de réponse et un message.
                        - code (int): Le code de statut HTTP (200 pour succès, 400 pour échec).
                        - message (str): Un message décrivant le résultat de l'opération.
    """

    response = {'code': 200, 'message': ''}

    # Vérifie que le joueur a un nom défini
    if 'player_name' not in session:
        return redirect(url_for('play'))

    # Initialise la structure de données si nécessaire
    if not isinstance(session['player_name'], dict):
        session['player_name'] = {'name': session['player_name'], 'team': []}

    elif 'team' not in session['player_name']:
        session['player_name']['team'] = []

    # Vérifie si le Pokémon est déjà dans l'équipe
    if pokemon_id in session['player_name']['team']:
        response['code'] = 400
        response['message'] = "Le Pokémon est déjà dans l'équipe."
        return response

    if len(session['player_name']['team']) < 5:
        # Ajoute le Pokémon à l'équipe
        session['player_name']['team'].append(pokemon_id)
        session.modified = True

    else:
        response['code'] = 400
        response['message'] = "L'équipe est déjà pleine."
        return response

    response['message'] = "Le Pokémon a été ajouté à l'équipe."
    return response

@app.route('/remove_pokemon_from_team/<int:pokemon_id>', methods=['DELETE'])
def remove_pokemon_from_team(pokemon_id):
    """
    Supprime un Pokémon de l'équipe du joueur.

    Args:
        pokemon_id (int): L'identifiant du Pokémon à supprimer.

    Returns:
        response (dict): Un dictionnaire contenant le code de réponse et un message.
                        - code (int): Le code de statut HTTP (200 pour succès, 400 pour échec).
                        - message (str): Un message décrivant le résultat de l'opération.

    Redirections:
        Si le nom du joueur n'est pas défini dans la session, redirige vers la page de jeu.
    """

    response = {'code': 200, 'message': ''}

    # Vérifie que le joueur a un nom défini
    if 'player_name' not in session:
        return redirect(url_for('play'))

    # Initialise la structure de données si nécessaire
    if not isinstance(session['player_name'], dict):
        session['player_name'] = {'name': session['player_name'], 'team': []}

    elif 'team' not in session['player_name']:
        session['player_name']['team'] = []

    # Retire le Pokémon de l'équipe
    if pokemon_id in session['player_name']['team']:
        session['player_name']['team'].remove(pokemon_id)
        session.modified = True

    else:
        response['code'] = 400
        response['message'] = "Le Pokémon n'est pas dans l'équipe."
        return response

    response['message'] = "Le Pokémon a été retiré de l'équipe."
    return response





TYPE_CHART = {
    
  "normal": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 1,
    "fighting": 1,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 1,
    "bug": 1,
    "rock": 0.5,
    "ghost": 0,
    "dragon": 1,
    "dark": 1,
    "steel": 0.5
  },
  "fire": {
    "normal": 1,
    "fire": 0.5,
    "water": 0.5,
    "electric": 1,
    "grass": 2,
    "ice": 2,
    "fighting": 1,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 1,
    "bug": 2,
    "rock": 0.5,
    "ghost": 1,
    "dragon": 0.5,
    "dark": 1,
    "steel": 2
  },
  "water": {
    "normal": 1,
    "fire": 2,
    "water": 0.5,
    "electric": 1,
    "grass": 0.5,
    "ice": 1,
    "fighting": 1,
    "poison": 1,
    "ground": 2,
    "flying": 1,
    "psychic": 1,
    "bug": 1,
    "rock": 2,
    "ghost": 1,
    "dragon": 0.5,
    "dark": 1,
    "steel": 1
  },
  "electric": {
    "normal": 1,
    "fire": 1,
    "water": 2,
    "electric": 0.5,
    "grass": 0.5,
    "ice": 1,
    "fighting": 1,
    "poison": 1,
    "ground": 0,
    "flying": 2,
    "psychic": 1,
    "bug": 1,
    "rock": 1,
    "ghost": 1,
    "dragon": 0.5,
    "dark": 1,
    "steel": 1
  },
  "grass": {
    "normal": 1,
    "fire": 0.5,
    "water": 2,
    "electric": 1,
    "grass": 0.5,
    "ice": 1,
    "fighting": 1,
    "poison": 0.5,
    "ground": 2,
    "flying": 0.5,
    "psychic": 1,
    "bug": 0.5,
    "rock": 2,
    "ghost": 1,
    "dragon": 0.5,
    "dark": 1,
    "steel": 0.5
  },
  "ice": {
    "normal": 1,
    "fire": 0.5,
    "water": 0.5,
    "electric": 1,
    "grass": 2,
    "ice": 0.5,
    "fighting": 1,
    "poison": 1,
    "ground": 2,
    "flying": 2,
    "psychic": 1,
    "bug": 1,
    "rock": 1,
    "ghost": 1,
    "dragon": 2,
    "dark": 1,
    "steel": 0.5
  },
  "fighting": {
    "normal": 2,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 2,
    "fighting": 1,
    "poison": 0.5,
    "ground": 1,
    "flying": 0.5,
    "psychic": 0.5,
    "bug": 0.5,
    "rock": 2,
    "ghost": 0,
    "dragon": 1,
    "dark": 2,
    "steel": 2
  },
  "poison": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 2,
    "ice": 1,
    "fighting": 1,
    "poison": 0.5,
    "ground": 0.5,
    "flying": 1,
    "psychic": 1,
    "bug": 1,
    "rock": 0.5,
    "ghost": 0.5,
    "dragon": 1,
    "dark": 1,
    "steel": 0
  },
  "ground": {
    "normal": 1,
    "fire": 2,
    "water": 1,
    "electric": 2,
    "grass": 0.5,
    "ice": 1,
    "fighting": 1,
    "poison": 2,
    "ground": 1,
    "flying": 0,
    "psychic": 1,
    "bug": 0.5,
    "rock": 2,
    "ghost": 1,
    "dragon": 1,
    "dark": 1,
    "steel": 2
  },
  "flying": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 0.5,
    "grass": 2,
    "ice": 1,
    "fighting": 2,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 1,
    "bug": 2,
    "rock": 0.5,
    "ghost": 1,
    "dragon": 1,
    "dark": 1,
    "steel": 0.5
  },
  "psychic": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 1,
    "fighting": 2,
    "poison": 2,
    "ground": 1,
    "flying": 1,
    "psychic": 0.5,
    "bug": 1,
    "rock": 1,
    "ghost": 1,
    "dragon": 1,
    "dark": 0,
    "steel": 0.5
  },
  "bug": {
    "normal": 1,
    "fire": 0.5,
    "water": 1,
    "electric": 1,
    "grass": 2,
    "ice": 1,
    "fighting": 0.5,
    "poison": 0.5,
    "ground": 1,
    "flying": 0.5,
    "psychic": 2,
    "bug": 1,
    "rock": 1,
    "ghost": 0.5,
    "dragon": 1,
    "dark": 2,
    "steel": 0.5
  },
  "rock": {
    "normal": 1,
    "fire": 2,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 2,
    "fighting": 0.5,
    "poison": 1,
    "ground": 0.5,
    "flying": 2,
    "psychic": 1,
    "bug": 2,
    "rock": 1,
    "ghost": 1,
    "dragon": 1,
    "dark": 1,
    "steel": 0.5
  },
  "ghost": {
    "normal": 0,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 1,
    "fighting": 1,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 2,
    "bug": 1,
    "rock": 1,
    "ghost": 2,
    "dragon": 1,
    "dark": 0.5,
    "steel": 0.5
  },
  "dragon": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 1,
    "fighting": 1,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 1,
    "bug": 1,
    "rock": 1,
    "ghost": 1,
    "dragon": 2,
    "dark": 1,
    "steel": 0.5
  },
  "dark": {
    "normal": 1,
    "fire": 1,
    "water": 1,
    "electric": 1,
    "grass": 1,
    "ice": 1,
    "fighting": 0.5,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 2,
    "bug": 1,
    "rock": 1,
    "ghost": 2,
    "dragon": 1,
    "dark": 0.5,
    "steel": 0.5
  },
  "steel": {
    "normal": 1,
    "fire": 0.5,
    "water": 0.5,
    "electric": 0.5,
    "grass": 1,
    "ice": 2,
    "fighting": 1,
    "poison": 1,
    "ground": 1,
    "flying": 1,
    "psychic": 1,
    "bug": 1,
    "rock": 2,
    "ghost": 1,
    "dragon": 1,
    "dark": 1,
    "steel": 0.5
  }
}




@app.route('/battle')
def battle():
    return render_template('battle.html')

def generate_random_team():
    """
    Génère une équipe aléatoire de 5 Pokémon pour le bot.
    """
    team = []
    while len(team) < 5:
        pokemon_id = random.randint(1, 151)
        if pokemon_id not in team:
            team.append(pokemon_id)
    return team


def calculate_damage(attacker, defender, attack_stat, defense_stat, base_power=50):
    """
    Calcule les dégâts d'une attaque en fonction des types et des statistiques.

    Args:
        attacker (dict): Données du Pokémon attaquant (inclut 'type').
        defender (dict): Données du Pokémon défenseur (inclut 'type').
        attack_stat (int): Statistique d'attaque de l'attaquant.
        defense_stat (int): Statistique de défense du défenseur.
        base_power (int): Puissance de l'attaque (par défaut 50).
    
    Returns:
        int: Dégâts infligés.
    """
    attacker_types = attacker['type'] if isinstance(attacker['type'], list) else [attacker['type']]
    defender_types = defender['type'] if isinstance(defender['type'], list) else [defender['type']]


    type_multiplier = 1
    for atk_type in attacker_types:
        for def_type in defender_types:
            type_multiplier *= TYPE_CHART.get(atk_type, {}).get(def_type, 1)


    damage = (((2 * 50 / 5 + 2) * base_power * (attack_stat / defense_stat)) / 50 + 2) * type_multiplier
    return max(1, int(damage)) 



@app.route('/start_battle', methods=['POST'])
def start_battle():
    if 'player_name' not in session or 'team' not in session['player_name']:
        return redirect(url_for('play'))
    

    def fetch_pokemon_data(team):
        """
        Récupère les données des Pokémon d'une équipe.
        
        Args:
            team (list): Liste des identifiants des Pokémon.
            
        Returns:
            data (list): Liste des données des Pokémon.
        """
        data = []
        for pokemon_id in team:
            pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()
            stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
            types = [t['type']['name'].capitalize() for t in pokemon['types']] 
            moves = []
            

            for move in pokemon['moves'][:4]:  # Limiter à 4 capacités pour l'affichage
                move_data = requests.get(move['move']['url']).json()
                moves.append({
                    'name': move['move']['name'].capitalize(),
                    'type': move_data['type']['name'].capitalize(),
                    'power': move_data['power'],
                    'effect': move_data.get('effect_entries', [{}])[0].get('short_effect', 'Pas d\'effet')
                })
            
            data.append({
                'name': pokemon['name'].capitalize(),
                'image': pokemon['sprites']['front_default'],
                'id': pokemon['id'],
                'hp': stats.get('hp', 100),
                'attack': stats.get('attack', 10),
                'defense': stats.get('defense', 10),
                'type': ', '.join(types), 
                'moves': moves  
            })
        return data



    player_team = session['player_name']['team']
    bot_team = generate_random_team()

    player_team_data = fetch_pokemon_data(player_team)
    bot_team_data = fetch_pokemon_data(bot_team)

    session['battle'] = {
        'player_team': player_team,
        'bot_team': bot_team,
        'player_team_data': player_team_data,
        'bot_team_data': bot_team_data,
        'turn': 'player',
        'player_hp': [pokemon['hp'] for pokemon in player_team_data],
        'bot_hp': [pokemon['hp'] for pokemon in bot_team_data],
        'active_pokemon': {
            'player': 0,
            'bot': random.randint(0, len(bot_team) - 1)
        }
    }

    return redirect(url_for('battle'))




@app.route('/battle_turn', methods=['POST'])
def battle_turn():
    if 'battle' not in session:
        return redirect(url_for('play'))

    battle = session['battle']
    turn = battle['turn']
    player_hp = battle['player_hp']
    bot_hp = battle['bot_hp']
    active_player_pokemon = battle['active_pokemon']['player']
    active_bot_pokemon = battle['active_pokemon']['bot']


    if all(hp <= 0 for hp in player_hp):
        battle['message'] = "Le bot a gagné !"
        battle['winner'] = 'bot'  
        session['battle'] = battle
        session.modified = True
        return redirect(url_for('battle'))

    if all(hp <= 0 for hp in bot_hp):
        battle['message'] = "Le joueur a gagné !"
        battle['winner'] = 'player'
        session['battle'] = battle
        session.modified = True
        return redirect(url_for('battle'))

    if turn == 'player':
        move_index = int(request.form.get('move')) 

        chosen_move = battle['player_team_data'][active_player_pokemon]['moves'][move_index]

        damage = calculate_damage(
            attacker=battle['player_team_data'][active_player_pokemon],
            defender=battle['bot_team_data'][active_bot_pokemon],
            attack_stat=battle['player_team_data'][active_player_pokemon]['attack'],
            defense_stat=battle['bot_team_data'][active_bot_pokemon]['defense'],
            base_power=chosen_move['power'] or 50  
        )
        bot_hp[active_bot_pokemon] -= damage
        battle['message'] = f"Vous avez infligé {damage} dégâts au Pokémon adverse avec {chosen_move['name']} !"

        if bot_hp[active_bot_pokemon] <= 0:
            bot_hp[active_bot_pokemon] = 0
            battle['message'] += " Le Pokémon du bot est KO !"
            next_pokemon = next((i for i, hp in enumerate(bot_hp) if hp > 0), None)
            if next_pokemon is not None:
                battle['active_pokemon']['bot'] = next_pokemon
            else:
                battle['message'] = "Le joueur a gagné !"
                battle['winner'] = 'player'
                session['battle'] = battle
                session.modified = True
                return redirect(url_for('battle'))

        battle['turn'] = 'bot'

    elif turn == 'bot':
        damage = calculate_damage(
            attacker=battle['bot_team_data'][active_bot_pokemon],
            defender=battle['player_team_data'][active_player_pokemon],
            attack_stat=battle['bot_team_data'][active_bot_pokemon]['attack'],
            defense_stat=battle['player_team_data'][active_player_pokemon]['defense']
        )
        player_hp[active_player_pokemon] -= damage
        battle['message'] = f"Le bot a infligé {damage} dégâts à votre Pokémon !"

        if player_hp[active_player_pokemon] <= 0:
            player_hp[active_player_pokemon] = 0
            battle['message'] += " Votre Pokémon est KO !"
            next_pokemon = next((i for i, hp in enumerate(player_hp) if hp > 0), None)
            if next_pokemon is not None:
                battle['active_pokemon']['player'] = next_pokemon
            else:
                battle['message'] = "Le bot a gagné !"
                battle['winner'] = 'bot'
                session['battle'] = battle
                session.modified = True
                return redirect(url_for('battle'))

        battle['turn'] = 'player'

    battle['player_hp'] = player_hp
    battle['bot_hp'] = bot_hp
    session['battle'] = battle
    session.modified = True

    return redirect(url_for('battle'))




@app.route('/use_move', methods=['POST'])
def use_move():
    if 'battle' not in session:
        return redirect(url_for('play'))

    battle = session['battle']
    player_team_data = battle['player_team_data']
    bot_team_data = battle['bot_team_data']
    active_player_pokemon = battle['active_pokemon']['player']
    active_bot_pokemon = battle['active_pokemon']['bot']
    player_hp = battle['player_hp']
    bot_hp = battle['bot_hp']

    move_name = request.form.get('move_name')

    chosen_move = None
    for move in player_team_data[active_player_pokemon]['moves']:
        if move['name'].lower() == move_name.lower():
            chosen_move = move
            break

    if not chosen_move:
        battle['message'] = "Le move choisi n'existe pas."
        session['battle'] = battle
        session.modified = True
        return redirect(url_for('battle'))

    # Le calcul ne prend pas en compte les effets des capacités comme les statuts (flemme)
    damage = calculate_damage(
        attacker=player_team_data[active_player_pokemon],
        defender=bot_team_data[active_bot_pokemon],
        attack_stat=player_team_data[active_player_pokemon]['attack'],
        defense_stat=bot_team_data[active_bot_pokemon]['defense'],
        base_power=chosen_move['power'] or 50
    )

    bot_hp[active_bot_pokemon] -= damage
    battle['message'] = f"Vous avez infligé {damage} dégâts au Pokémon adverse avec {chosen_move['name']} !"

    if bot_hp[active_bot_pokemon] <= 0:
        bot_hp[active_bot_pokemon] = 0
        battle['message'] += " Le Pokémon du bot est KO !"
        next_pokemon = next((i for i, hp in enumerate(bot_hp) if hp > 0), None)
        if next_pokemon is not None:
            battle['active_pokemon']['bot'] = next_pokemon
        else:
            battle['message'] = "Le joueur a gagné !"
            battle['winner'] = 'player'
            session['battle'] = battle
            session.modified = True
            return redirect(url_for('battle'))

    battle['turn'] = 'bot'

    battle['player_hp'] = player_hp
    battle['bot_hp'] = bot_hp
    session['battle'] = battle
    session.modified = True

    return redirect(url_for('battle'))

















@app.route('/choose_pokemon', methods=['POST'])
def choose_pokemon():
    if 'battle' not in session:
        return redirect(url_for('play'))

    try:
        # Récupérer l'index du Pokémon sélectionné
        new_active = int(request.form.get('pokemon_index'))
    except (TypeError, ValueError):
        # Rediriger en cas de problème avec l'index
        return redirect(url_for('battle'))

    battle = session['battle']

    # Vérification de la validité de l'index
    if new_active < 0 or new_active >= len(battle['player_team']):
        # Si l'index est invalide, on redirige avec un message d'erreur
        battle['message'] = "Index du Pokémon invalide."
        session['battle'] = battle
        return redirect(url_for('battle'))

    # Changer le Pokémon actif pour le joueur
    battle['active_pokemon']['player'] = new_active
    battle['message'] = f"{battle['player_team_data'][new_active]['name']} est envoyé au combat !"

    # Sauvegarder les modifications dans la session
    session['battle'] = battle
    session.modified = True

    return redirect(url_for('battle'))











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