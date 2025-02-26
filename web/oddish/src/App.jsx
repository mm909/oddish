import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'

import { AhkProvider } from './contexts/ahk';

import Navagation from './components/navagation/navagation'
import Running from './pages/Running'
import NotFound from './pages/not_found'
import AppleHealthKitSummary from './pages/apple_health_kit_summary'
import QuantitiesGraphs from './pages/quantities_graphs'
import ElevationGraphs from './pages/elevation_graphs'
import RunList from './pages/run_list'
import LOLOddOneOut from './pages/lol_odd_one_out'

function App() {

  return (
    <>
      <AhkProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Navagation />}>
              <Route path="running" element={<Running />} />
              <Route path="RunList" element={<RunList />} />
              <Route path="AHKSummary" element={<AppleHealthKitSummary />} />
              <Route path="QuantitiesGraphs" element={<QuantitiesGraphs />} />
              <Route path="ElevationGraphs" element={<ElevationGraphs />} />
              <Route path="LOLOddOneOut" element={<LOLOddOneOut />} />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </Router>
      </AhkProvider>
    </>
  )
}

export default App
