import React from 'react'
import { Link } from 'react-router-dom'

function LinkMenuBase({ title, links }) {
    return (
        <div className='flex-1'>
            <div className='flex flex-col'>
                <div className='my-[20px]'>
                    <div className='text-[12px] mb-[12px] opacity-50'>
                        {title}
                    </div>
                    <ul>
                        {links.map((link, index) => (
                            <li key={index} className=' text-wrap mb-[5px]'>
                                <Link to={link.href}>{link.text}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default LinkMenuBase
