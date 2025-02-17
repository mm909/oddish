import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'

import Navagation from './components/navagation/navagation'
import Running from './pages/Running'
import NotFound from './pages/not_found'
import AppleHealthKitSummary from './pages/apple_health_kit_summary'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Navagation />}>
            <Route path="running" element={<Running />} />
            <Route path="AHKSummary" element={<AppleHealthKitSummary />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
