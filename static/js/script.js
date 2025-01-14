if (window.location.pathname === '/') {
    const socket = io.connect();
    const container = document.getElementById('pokemon-container');
    const loadingElement = document.getElementById('loading');
    let allPokemons = [];  // Array to store all Pokémon data
    let firstPokemonDisplayed = false;  // Flag to check if the first Pokémon is displayed

    // Search Pokémon by name
    function searchPokemon() {
        const searchTerm = document.getElementById('search-bar').value.toLowerCase();
        container.innerHTML = '';  // Clear the container before filtering

        const filteredPokemons = allPokemons.filter(pokemon =>
            pokemon.name.toLowerCase().includes(searchTerm)
        );

        filteredPokemons.forEach(pokemon => {
            const card = document.createElement('div');
            card.classList.add('pokemon-card');
            card.id = pokemon.id;
            card.onclick = () => {
                getPokemonInfo(pokemon.id);
            };

            const nameElement = document.createElement('h2');
            nameElement.textContent = pokemon.name;

            const imageElement = document.createElement('img');
            imageElement.src = pokemon.image;
            imageElement.alt = pokemon.name;

            card.appendChild(imageElement);
            card.appendChild(nameElement);
            container.appendChild(card);
        });
    }

    function getPokemonInfo(pokemonId) {
        let pokemonInfoContainer = document.getElementById('pokemon-info');
        fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                pokemonInfoContainer.innerHTML = `
                    <h2 class="pokemon-name">${data.name}</h2>
                    <div class="pokemon-image-container">
                        <img class="pokemon-image" src="${data.sprites.front_default}" alt="${data.name}" />
                    </div>
    
                    <div class="pokemon-details">
                        <div class="pokemon-detail">
                            <strong>Height:</strong> <span>${data.height} decimetres</span>
                        </div>
                        <div class="pokemon-detail">
                            <strong>Weight:</strong> <span>${data.weight} hectograms</span>
                        </div>
                        <div class="pokemon-detail">
                            <strong>Base Experience:</strong> <span>${data.base_experience}</span>
                        </div>
                    </div>
    
                    <div class="pokemon-abilities">
                        <strong>Abilities:</strong>
                        <span>${data.abilities.map(ability => ability.ability.name).join(', ')}</span>
                    </div>
    
                    <div class="pokemon-types">
                        <strong>Types:</strong>
                        <span>
                            ${data.types.map(type => `<span class="pokemon-type ${type.type.name}">${type.type.name}</span>`).join(', ')}
                        </span>
                    </div>
    
                    <div class="pokemon-stats">
                        <strong>Stats:</strong>
                        <ul>
                            ${data.stats.map(stat => `
                                <li>
                                    ${stat.stat.name}: 
                                    <div class="stat-bar">
                                        <div class="stat-bar-fill" style="width: ${stat.base_stat}%"></div>
                                    </div>
                                    <span>${stat.base_stat}</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>   
                    
                    <form action="/add_pokemon_to_team/${data.id}" method="POST">
                        <button type="submit" class="form-button">Ajouter à l'équipe</button>
                    </form>
                    `;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    // Show loading element
    loadingElement.style.display = 'flex';
    
    // Request Pokémon data
    socket.emit('get_pokemons');
    
    // Add Pokémon to the container one by one
    socket.on('pokemon_data', (pokemon) => {
        allPokemons.push(pokemon);  // Store each Pokémon in the array
        const card = document.createElement('div');
        card.classList.add('pokemon-card');
        card.id = pokemon.id;
        card.onclick = () => {
            getPokemonInfo(pokemon.id);
        };
    
        const nameElement = document.createElement('h2');
        nameElement.textContent = pokemon.name;
    
        const imageElement = document.createElement('img');
        imageElement.src = pokemon.image;
        imageElement.alt = pokemon.name;
    
        card.appendChild(imageElement);
        card.appendChild(nameElement);
        container.appendChild(card);
    
        // Hide loading element after the first Pokémon is added
        if (!firstPokemonDisplayed) {
            loadingElement.style.display = 'none';
            firstPokemonDisplayed = true;
        }
    });

    document.querySelector('.carousel-button[onclick="scrollCarousel(-1)"]').addEventListener('click', () => scrollCarousel(-1));
    document.querySelector('.carousel-button[onclick="scrollCarousel(1)"]').addEventListener('click', () => scrollCarousel(1));
    document.getElementById('search-bar').addEventListener('input', searchPokemon);

    // Scroll Function for Carousel Navigation
    function scrollCarousel(direction) {
        container.scrollBy({
            left: direction * 200, // Scrolls by 200px per click
            behavior: 'smooth',
        });
    }
}

// FONCTIONS PERMETTANT DE RECUPERER LES DONNEES DES POKEMONS DE l'EQUIPE
// ET DE LES AFFICHER DANS LA PAGE


// Fonction permettant de récupérer les données des pokemons de l'équipe et de les afficher dans la page
if (window.location.pathname === '/play') {

    // Fonction permettant de récupérer les données des pokemons de l'équipe
    const pokemonTeamContainer = document.querySelector('.pokemon-team');
    console.log('play');
    fetch('/get_pokemon_team')
    .then(
        response => response.json()
    )
    .then(
        data => {
            console.log(data);
            if (data.length > 0) {
                data.forEach(pokemon => {
                    fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        const card = document.createElement('div');
                        card.classList.add('pokemon-card');
                        card.id = data.id;

                        const nameElement = document.createElement('h2');
                        nameElement.textContent = data.name;

                        const imageElement = document.createElement('img');
                        imageElement.src = data.sprites.front_default;
                        imageElement.alt = data.name;

                        const removeButton = document.createElement('button');
                        removeButton.textContent = 'Supprimer';
                        removeButton.onclick = () => {
                            fetch(`/remove_pokemon_from_team/${data.id}`, {
                                method: 'DELETE',
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log(data);
                                card.remove();
                            })
                            .catch(error => console.error('Error:', error));
                        }
                        removeButton.classList.add('form-button');

                        card.appendChild(imageElement);
                        card.appendChild(nameElement);
                        card.appendChild(removeButton);
                        pokemonTeamContainer.appendChild(card);
                    })
                })
            }
            
        }
    )
    .catch(error => console.error('Error:', error));
}