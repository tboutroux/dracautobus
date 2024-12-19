const socket = io.connect();
const container = document.getElementById('pokemon-container');
const loadingElement = document.getElementById('loading');
let allPokemons = [];  // Array to store all Pokémon data
let firstPokemonDisplayed = false;  // Flag to check if the first Pokémon is displayed

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

// Scroll Function for Carousel Navigation
function scrollCarousel(direction) {
    container.scrollBy({
        left: direction * 200, // Scrolls by 200px per click
        behavior: 'smooth',
    });
}

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
                    <span>${data.types.map(type => type.type.name).join(', ')}</span>
                </div>

                <div class="pokemon-stats">
                    <strong>Stats:</strong>
                    <ul>
                        ${data.stats.map(stat => `<li>${stat.stat.name}: ${stat.base_stat}</li>`).join('')}
                    </ul>
                </div>   `;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

document.querySelector('.carousel-button[onclick="scrollCarousel(-1)"]').addEventListener('click', () => scrollCarousel(-1));
document.querySelector('.carousel-button[onclick="scrollCarousel(1)"]').addEventListener('click', () => scrollCarousel(1));
document.getElementById('search-bar').addEventListener('input', searchPokemon);