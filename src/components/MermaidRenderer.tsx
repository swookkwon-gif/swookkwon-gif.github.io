"use client";

import React, { useEffect, useState, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({
  startOnLoad: false,
  theme: "default",
  securityLevel: "loose",
  fontFamily: "inherit",
});

let idCounter = 0;

export default function MermaidRenderer({ chart }: { chart: string }) {
  const [svg, setSvg] = useState<string>("");
  const id = useRef(`mermaid-${Date.now()}-${idCounter++}`).current;

  useEffect(() => {
    let isMounted = true;
    
    async function renderChart() {
      try {
        const { svg: renderedSvg } = await mermaid.render(id, chart);
        if (isMounted) {
          setSvg(renderedSvg);
        }
      } catch (error) {
        console.error("Mermaid rendering failed:", error);
      }
    }
    
    renderChart();
    
    return () => {
      isMounted = false;
    };
  }, [chart, id]);

  if (!svg) {
    return <div className="animate-pulse bg-gray-100 rounded-lg h-40 flex items-center justify-center text-gray-400 text-sm">Loading diagram...</div>;
  }

  return (
    <div 
      className="my-8 flex justify-center bg-white p-6 rounded-xl shadow-sm border border-gray-100 overflow-x-auto" 
      dangerouslySetInnerHTML={{ __html: svg }} 
    />
  );
}
