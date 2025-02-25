import React from 'react'

import Stat from './stat'
import GPXSVGMap from '../maps/gpx_svg_map'

function RunListSummary({n, run}) {

    // format start date like December 22, 2023
    let start_date_formatted = new Date(run.start_date).toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'});


    // run duration starts as "1.23123" this is how many min the run was, we want to convert it to "01:23:12"
    let run_duration = run.duration;
    let run_duration_hours = Math.floor(run_duration / 60);
    let run_duration_minutes = Math.floor(run_duration % 60).toString().padStart(2, '0');
    let run_duration_seconds = Math.floor((run_duration * 60) % 60).toString().padStart(2, '0');
    run_duration = `${run_duration_hours}:${run_duration_minutes}:${run_duration_seconds}`;

    let total_distance = Number(run.total_distance); // Miles
    let run_duration_seconds_total = run.duration * 60; // Total duration in seconds
    let pace_seconds_per_mile = run_duration_seconds_total / total_distance;
    let pace_minutes = Math.floor(pace_seconds_per_mile / 60);
    let pace_seconds = Math.floor(pace_seconds_per_mile % 60).toString().padStart(2, '0');
    let pace = `${pace_minutes}:${pace_seconds}/mi`;

    let elevation = run.elevation_ascended;
    // elevation is current "xxxxx cm" conver to xxxxx m
    // remove " cm"
    if (elevation === undefined) {
        elevation = '0 cm';
    }
    elevation = elevation.replace(' cm', '');
    elevation = Number(elevation);

    // convert cm to m

    let elevation_value = (elevation / 100).toFixed(0) + "m";
    

  return (
    <>
        <div className='
            border border-transparent hover:border-gray-300
            rounded-lg
            p-[5px]
        ' onClick={() => {console.log(run);
        }}>
            <div className='
                text-[20px]
            '>
                {/* {start_date_formatted} */}
            </div>
            <div>
                <div className='
                    flex
                    gap-[5px]
                '>
                    <div className='
                    flex 
                    flex-grow
                    '>
                        <GPXSVGMap run={run} />
                    </div>
                    {/* <div>
                        <div className='
                            flex
                            flex-col
                        '>
                            <Stat label='Distance' value={Number(run.total_distance).toFixed(2) + "mi"} />
                            <Stat label='Duration' value={run_duration} />
                            <Stat label='Average Pace' value={pace} />
                            <Stat label='Average Heart Rate' value={Number(run.heart_rate_average).toFixed(0) + "bpm"} />
                            <Stat label='Elevation' value={elevation_value} />

                        </div>
                    </div> */}
                </div>
                {/* Route {n} - #{n} */}
            </div>

        </div>
    </>

  )
}

export default RunListSummary
