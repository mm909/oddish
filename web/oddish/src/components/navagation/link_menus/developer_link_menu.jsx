import React from 'react'
import LinkMenuBase from './link_menu_base'

function DeveloperLinkMenu() {
  return (
    <>
      <div className='flex justify-center flex-1  space-x-4'>
        <LinkMenuBase title='Health' links={[
          { href: '/AHKSummary', text: 'Apple Health Kit Summary' },
          { href: '/QuantitiesGraphs', text: 'Quantities Graphs' },
          { href: '/ElevationGraphs', text: 'Elevation Graphs' },
        ]} className='flex-1' />
      </div>
    </>
  )
}

export default DeveloperLinkMenu