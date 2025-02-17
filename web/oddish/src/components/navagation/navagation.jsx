import React from 'react'
import { Outlet } from 'react-router-dom'

import TitleBar from './title_bar'
import LinkBar from './link_bar'

function Navagation() {

  return (
    <>
        <div className='absolute top-0 right-0 w-[100%]'>
          <div className='flex flex-col w-[60%] mx-auto'>
            <TitleBar />
            <LinkBar />
          </div>
        </div>
        <div className='mt-[75px] w-[60%] mx-auto'>
          <Outlet />
        </div>
    </>

  )
}

export default Navagation
