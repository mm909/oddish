import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function GPXSVGMap({ run }) {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 200;
    const height = 200;
    const margin = { top: 10, right: 10, bottom: 10, left: 10 };

    svg.attr('viewBox', `0 0 ${width} ${height}`)
       .attr('preserveAspectRatio', 'xMidYMid meet');

    const trackData = Object.values(run.track_data).filter(d => d.lat !== undefined && d.lon !== undefined);

    const x = d3.scaleLinear()
      .domain(d3.extent(trackData, d => d.lon))
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain(d3.extent(trackData, d => d.lat))
      .range([height - margin.bottom, margin.top]);

    const line = d3.line()
      .x(d => x(d.lon))
      .y(d => y(d.lat));

    svg.selectAll('*').remove(); // Clear previous content

    svg.append('path')
      .datum(trackData)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 4)
      .attr('d', line);

  }, [run]);

  return (
    <svg ref={svgRef} width="100%" height="100%"></svg>
  );
}

export default GPXSVGMap;