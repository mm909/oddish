import React from 'react';

function Button1({ onClick, children }) {
  return (
      <div 
        className='
          cursor-pointer
          border-[1px]
          hover:border-[2px]
          border-black
          border-opacity-30
          rounded 
          py-[8px] 
          hover:py-[7px]
          px-[16px] 
          hover:px-[15px]
          select-none
        '
        onClick={onClick}
      >
        {children}
      </div>
  );
}

export default Button1;