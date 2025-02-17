import React from 'react'
import { useState, useEffect } from 'react'
import PokemonPlaceholder from '../components/fun/pokemon_placeholder'

function NotFound() {
  return (
    <>
      <PokemonPlaceholder id={404} />
    </>
  )
}

export default NotFound
