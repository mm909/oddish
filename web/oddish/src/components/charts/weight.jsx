import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import 'd3-interpolate-path';

const WeightChart = ({ data, quantity }) => {
  const svgRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

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

  useEffect(() => {
    if (dimensions.width === 0 || dimensions.height === 0) return;

    const svg = d3.select(svgRef.current);
    const { width, height } = dimensions;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };

    svg.selectAll('*').remove(); // Clear previous content

    svg.attr('width', width).attr('height', height);

    const parsedData = Object.keys(data).map(date => ({
      date: new Date(date),
      value: data[date][quantity]
    })).filter(d => d.value !== undefined);

    const x = d3.scaleTime()
      .domain(d3.extent(parsedData, d => d.date))
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([d3.min(parsedData, d => d.value) - 1, d3.max(parsedData, d => d.value) + 1])
      .nice()
      .range([height - margin.bottom, margin.top]);

    const line = d3.line()
      .x(d => x(d.date))
      .y(d => y(d.value));

    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    const path = svg.append('path')
      .datum(parsedData)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 1.5)
      .attr('d', line);

    // Add transition for smooth update
    path.transition()
      .duration(750)
      .attrTween('d', function() {
        const previous = d3.select(this).attr('d');
        const current = line(parsedData);
        const interpolate = d3.interpolate(previous, current);
        return t => interpolate(t);
      });

  }, [data, dimensions, quantity]);

  return (
    <div ref={containerRef} className="w-full h-full">
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default WeightChart;