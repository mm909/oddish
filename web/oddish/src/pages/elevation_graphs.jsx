import React, { useEffect, useRef } from 'react';

import { useState } from 'react';
import * as d3 from 'd3';
import ahk from '../ahk/ahk.json';

function ElevationGraph() {
  const svgRef = useRef();
  const containerRef = useRef();
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  

  let keys = [
    '88FA0020-967D-4964-A410-FFEB62480BFD',
    '9D199C8C-F1A8-4BBC-9956-4BB4BE5E3592',
    // 'D535DA30-AE64-4154-8E54-2094E8C3F3F8',
    // '17828B3A-91A7-44E4-80FA-B267402FF00F',
    // '4478DF35-ED43-4659-A23C-69524E0D565C',
  ];

  let runs = ahk.runs.filter(run => keys.includes(run.HKMetadataKeySyncIdentifier));

    useEffect(() => {
      const handleResize = () => {
        if (containerRef.current) {
          const { width, height } = containerRef.current.getBoundingClientRect();
          setDimensions({ width, height });
        }
      };
  
      window.addEventListener('resize', handleResize);
      handleResize(); // Initial call to set dimensions
      return () => window.removeEventListener('resize', handleResize);
  }, []);

  let data = runs.map(run => {
    return Object.entries(run.track_data).map(([timestamp, data]) => ({
      time: new Date(timestamp),
      elevation: data.ele
    })).filter(d => !isNaN(d.time) && !isNaN(d.elevation));
  });

  data.forEach(series => {
    let start = series[0].time;
    series.forEach(d => {
      d.time = (d.time - start) / 1000;
    });
  });


  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };

    svg.attr('viewBox', [0, 0, width, height]);

    const x = d3.scaleTime()
      .domain(d3.extent(data.flat(), d => d.time))
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([d3.min(data.flat(), d => d.elevation), d3.max(data.flat(), d => d.elevation)]).nice()
      .range([height - margin.bottom, margin.top]);

    const line = d3.line()
      .x(d => x(d.time))
      .y(d => y(d.elevation));

    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    data.forEach((series, index) => {
      svg.append('path')
        .datum(series)
        .attr('fill', 'none')
        .attr('stroke', d3.schemeCategory10[index % 10])
        .attr('stroke-width', 1.5)
        .attr('d', line);
    });

  }, [data]);

  return (
    <div ref={containerRef} className="w-full h-full">
    <svg ref={svgRef}></svg>
  </div>
  );
}

export default ElevationGraph;