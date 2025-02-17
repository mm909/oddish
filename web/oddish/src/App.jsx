import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'

import Navagation from './components/navagation/navagation'
import Ludwig from './pages/Ludwig'
import Running from './pages/Running'
import NotFound from './pages/not_found'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Navagation />}>
            <Route path="ludwig" element={<Ludwig />} />
            <Route path="running" element={<Running />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
