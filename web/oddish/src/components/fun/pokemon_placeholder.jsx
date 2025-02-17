import React from 'react'
import { useState, useEffect } from 'react'

/*
  Todo:
  - Add an option to not hit the API
  - Decide if all this state is needed
    - Whats the correct amount?  
*/

function PokemonPlaceholder({id, description}) {

  description = description || 'I don\'t think you\'re supposed to see this Pokémon.';

  const [pokemonId, setPokemonId] = useState(id || Math.floor(Math.random() * 649) + 1);
  const [pokemonData, setPokemonData] = useState(null);
  const [pokemonName, setPokemonName] = useState(null);
  const [pokemonNameEng, setPokemonNameEng] = useState(null);
  const [pokemonFlavorText, setPokemonFlavorText] = useState(null);
  const [imageLoaded, setImageLoaded] = useState(false);

  const pokemonId_formated = pokemonId.toString().padStart(3, '0');

  useEffect(() => {
    fetch(`https://pokeapi.co/api/v2/pokemon-species/${pokemonId}/`)
      .then(response => response.json())
      .then(data => {
        setPokemonData(data);

        const names = data.names;
        const flavorTextEntries = data.flavor_text_entries;
        const possibleLanguages = names.map(name => name.language.name)
          .filter(language => flavorTextEntries.some(entry => entry.language.name === language));

        setPokemonNameEng(names.find(name => name.language.name === 'en').name);

        if (possibleLanguages.length > 0) {
          const selectedLanguage = possibleLanguages[Math.floor(Math.random() * possibleLanguages.length)];
          const nameEntry = names.find(name => name.language.name === selectedLanguage);
          const flavorTextEntry = flavorTextEntries.find(entry => entry.language.name === selectedLanguage);
        
          if (nameEntry) {
            setPokemonName(nameEntry.name);
          }

          if (flavorTextEntry) {
            setPokemonFlavorText(flavorTextEntry.flavor_text);
          }
        }
      })
      .catch(error => console.error('Error fetching data:', error));
  }, [pokemonId]);

  const handleClick = () => {
    setPokemonId(Math.floor(Math.random() * 649) + 1);
  };

  const PokemonLoading = () => (
    <div className='flex flex-col gap-[5px]'>
      <div className='w-[300px] h-[300px] bg-gray-400 bg-opacity-75 animate-pulse' />
      <div className='w-[100px] h-[20px] bg-gray-300 bg-opacity-75 animate-pulse' />
      <div className='w-[300px] h-[12px] bg-gray-200 bg-opacity-75 animate-pulse' />
      <div className='w-[300px] h-[12px] bg-gray-200 bg-opacity-75 animate-pulse' />
      <div className='w-[300px] h-[12px] bg-gray-200 bg-opacity-75 animate-pulse' />
    </div>
  )

  return (
    <>
      <div className='flex flex-col items-center'>
        <div className='flex flex-col w-[300px]'>
          <div 
            className='text-[100px] leading-none select-none text-[#44729c] hover:text-opacity-90 w-fit'
            onClick={handleClick}
          >
            {pokemonId_formated}
          </div>
          <div className='text-[16px] my-[20px]'>
            {pokemonData && pokemonData.id === 404 ? description : ''} 
          </div>
          <div className='max-w-[300px] min-w-[300px] flex justify-center'>
            <img 
              src={`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/${pokemonId}.svg`} 
              alt={`Image of ${pokemonNameEng}, Pokémon number ${pokemonId}`} 
              className='object-contain'
              onLoad={() => setImageLoaded(true)}
            />
          </div>
          {imageLoaded ? (
            <div className='flex flex-col gap-[5px]'>
              <div>
                <a href={`https://pokemondb.net/pokedex/${pokemonNameEng}`} target='_blank' rel='noreferrer' className='text-black underline'>
                  {pokemonName}
                </a>
              </div>
              <div className='text-black text-opacity-60'>
                {pokemonFlavorText}
              </div>
            </div>
          ) : (
            <PokemonLoading />
          )}
        </div>
      </div>
    </>
  )
}

export default PokemonPlaceholder