import React from 'react'

import LinkMenuBase from './link_menu_base'

function RunningLinkMenu() {
  return (
    <>
      <div className='flex justify-center flex-1  space-x-4'>
        <LinkMenuBase title='Title' links={[
          { href: '/404', text: 'Short Option' }, 
        ]} className='flex-1' />

      </div>
    </>
  )
}

export default RunningLinkMenu