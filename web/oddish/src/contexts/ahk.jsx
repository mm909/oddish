import React, { createContext, useContext } from 'react';
import ahk from '../ahk/ahk.json';

const AhkContext = createContext();

export const AhkProvider = ({ children }) => {
  return (
    <AhkContext.Provider value={ahk}>
      {children}
    </AhkContext.Provider>
  );
};

export const useAhk = () => {
  return useContext(AhkContext);
};