import React from 'react'
import PrimaryLink from './primary_link'
import RunningLinkMenu from './link_menus/running_link_menu';
import DeveloperLinkMenu from './link_menus/developer_link_menu';
import { useState, useEffect, useRef } from 'react';
import './link_bar.css'; // Import the CSS file

function LinkBar() {
  const [hoveredLink, setHoveredLink] = useState(null);
  const [menuHeight, setMenuHeight] = useState(0);
  const menuRef = useRef(null);

  useEffect(() => {
    if (menuRef.current) {
      setMenuHeight(menuRef.current.offsetHeight);
    }
  }, [hoveredLink]);

  return (
    <>
      <div
        className={`
          border-y-[1px] border-black border-opacity-30 
          transition-all 
          bg-[#FFFBF0] overflow-hidden
        `}
        onClick={() => setHoveredLink(null)}
        onMouseLeave={() => setHoveredLink(null)}
        style={{ height: hoveredLink ? `${menuHeight + 30}px` : '30px', transition: 'height 0.3s ease' }}
      >
        <div className='flex justify-center items-center space-x-[20px] h-[30px]'>
          <PrimaryLink link='Running' onMouseEnter={() => setHoveredLink('Running menue')} />
          <PrimaryLink link='Developer' onMouseEnter={() => setHoveredLink('Developer menue')} />
        </div>
        <div ref={menuRef} className={`fade-transition ${hoveredLink ? 'fade-in' : 'fade-out'} w-[80%] mx-auto`}>
          {hoveredLink === 'Running menue' && <RunningLinkMenu />}
          {hoveredLink === 'Developer menue' && <DeveloperLinkMenu />}
        </div>
      </div>
    </>
  );
}

export default LinkBar;