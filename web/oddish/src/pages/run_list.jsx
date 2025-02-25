import React from 'react'
import RunListSummary from '../components/run/run_summary/run_list_summary'

import { useAhk } from '../contexts/ahk';

function RunList() {

    const ahk = useAhk();
    let runList = ahk.runs;
    runList = runList.sort((a, b) => new Date(b.start_date) - new Date(a.start_date));

    return (
    <>
      <div className="grid grid-cols-12 gap-4 p-4">
        {runList.map((run, index) => (
          <RunListSummary key={index} n={runList.length - index} run={run} />
        ))}
      </div>

    </>

  )
}

export default RunList
