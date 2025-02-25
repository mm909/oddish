import React from 'react'

function stat({label, value}) {
    return (
    <>
        <div className='
            text-[12px]
        '>
            {label}
        </div>
        <div className='
            text-[20px]
        '>
            {value}
        </div>
    </>

  )
}

export default stat
