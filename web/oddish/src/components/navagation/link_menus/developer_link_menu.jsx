import React from 'react'
import LinkMenuBase from './link_menu_base'

function DeveloperLinkMenu() {
  return (
    <>
      <div className='flex justify-center flex-1  space-x-4'>
        <LinkMenuBase title='Running' links={[
          { href: '/AHKSummary', text: 'Apple Health Kit Summary' },
        ]} className='flex-1' />
      </div>
    </>
  )
}

export default DeveloperLinkMenu