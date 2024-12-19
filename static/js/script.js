

function getPokemonInfo(pokemonId) {
    let pokemonInfoContainer = document.getElementById('pokemon-info');
    fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            pokemonInfoContainer.innerHTML = `
                <h2>${data.name}</h2>
                <img src="${data.sprites.front_default}" alt="${data.name}" />
                <p>Height: ${data.height}</p>
                <p>Weight: ${data.weight}</p>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

export default getPokemonInfo;