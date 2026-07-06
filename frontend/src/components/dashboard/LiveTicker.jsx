import React, { useEffect, useState } from "react";
import { usePriceStore } from "../../store/priceStore";
import { formatCurrency } from "../../utils/formatCurrency";
import { formatPercent } from "../../utils/formatPercent";
import { PRICE_STALE_AFTER_MS } from "../../constants/APP_CONFIG";

const LiveTicker = ({ ticker }) => {
  const priceData = usePriceStore((state) => state.livePrices[ticker]);
  const [isStale, setIsStale] = useState(false);

  useEffect(() => {
    if (!priceData?.updatedAt) return;

    const interval = setInterval(() => {
      const timeSinceUpdate = Date.now() - priceData.updatedAt;
      setIsStale(timeSinceUpdate > PRICE_STALE_AFTER_MS);
    }, 1000);

    return () => clearInterval(interval);
  }, [priceData?.updatedAt]);

  if (!priceData) {
    return (
      <div className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
        <span className="font-bold text-gray-900">{ticker}</span>
        <span className="text-sm text-gray-400">Waiting for data...</span>
      </div>
    );
  }

  const isPositive = priceData.change >= 0;
  const colorClass = isPositive ? "text-green-600" : "text-red-600";
  const bgClass    = isPositive ? "bg-green-50" : "bg-red-50";

  return (
    <div className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
      <div>
        <div className="flex items-center space-x-2">
          <span className="font-bold text-gray-900">{ticker}</span>
          {isStale && <span className="text-[10px] uppercase bg-gray-200 text-gray-600 px-1.5 py-0.5 rounded font-semibold">Stale</span>}
          {!isStale && <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />}
        </div>
        <div className={`text-xs font-medium mt-0.5 px-1.5 py-0.5 rounded inline-block ${colorClass} ${bgClass}`}>
          {formatPercent(priceData.changePercent)}
        </div>
      </div>
      <div className="text-right">
        <div className="font-semibold text-gray-900">{formatCurrency(priceData.price)}</div>
        <div className={`text-xs ${colorClass}`}>{priceData.change > 0 ? "+" : ""}{formatCurrency(priceData.change)}</div>
      </div>
    </div>
  );
};

export default LiveTicker;
