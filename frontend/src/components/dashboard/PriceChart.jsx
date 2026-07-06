import React, { useEffect, useRef, useState } from "react";
import { createChart, ColorType } from "lightweight-charts";

// For demo purposes, we will mock some historical data, since the backend
// only provides live socket updates (price_update), not historical candles.
const generateMockData = () => {
  let time = Math.floor(Date.now() / 1000) - 86400 * 30; // 30 days ago
  let price = 150;
  const data = [];
  for (let i = 0; i < 30; i++) {
    time += 86400;
    const open = price + (Math.random() - 0.5) * 5;
    const high = open + Math.random() * 5;
    const low = open - Math.random() * 5;
    const close = low + Math.random() * (high - low);
    data.push({ time, open, high, low, close });
    price = close;
  }
  return data;
};

const PriceChart = () => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRef = useRef(null);
  const [data] = useState(generateMockData());

  useEffect(() => {
    if (!chartContainerRef.current) return;

    chartRef.current = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#6B7280",
      },
      grid: {
        vertLines: { color: "#F3F4F6" },
        horzLines: { color: "#F3F4F6" },
      },
      width: chartContainerRef.current.clientWidth,
      height: 250,
    });

    seriesRef.current = chartRef.current.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });

    seriesRef.current.setData(data);
    chartRef.current.timeScale().fitContent();

    const handleResize = () => {
      chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chartRef.current.remove();
    };
  }, [data]);

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-2">30-Day Trend (Mock)</h3>
      <div ref={chartContainerRef} className="w-full" />
    </div>
  );
};

export default PriceChart;
