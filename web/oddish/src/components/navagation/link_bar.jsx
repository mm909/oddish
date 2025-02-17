import React from 'react'
import PrimaryLink from './primary_link'

function LinkBar() {

  const [hoveredLink, setHoveredLink] = React.useState("asdf");


  return (
    <>
      <div className='
        border-y-[1px] border-black border-opacity-30 
        hover:h-[100px] h-[25px] transition-all 
        bg-[#FFFBF0] overflow-hidden
      '>
        <div className='flex justify-center space-x-4'>
          <PrimaryLink link='Running' onMouseEnter={() => setHoveredLink('Running')} onMouseLeave={() => setHoveredLink(null)} />
          <PrimaryLink link='Geography' onMouseEnter={() => setHoveredLink('Geography')} onMouseLeave={() => setHoveredLink(null)} />
          <PrimaryLink link='Ludwig' onMouseEnter={() => setHoveredLink('Ludwig')} onMouseLeave={() => setHoveredLink(null)} />
        </div>
        <div>
          {hoveredLink}
        </div>
      </div>
      
    </>
  )
}

export default LinkBar
