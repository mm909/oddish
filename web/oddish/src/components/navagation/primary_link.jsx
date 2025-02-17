import React from 'react'
import { Link } from 'react-router-dom'

function PrimaryLink({link = 'Untitled', onMouseEnter, onMouseLeave}) {
  return (
    <>
        <Link to={`/${link.toLowerCase()}`} className='text-[16px]'  onMouseEnter={onMouseEnter} onMouseLeave={onMouseLeave}>
            {link}
        </Link>
    </>
  )
}

export default PrimaryLink
