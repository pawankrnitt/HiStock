import React from "react";

const MetricsPanel = () => {
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-gray-50 p-3 rounded-lg">
        <div className="text-xs text-gray-500 mb-1">P/E Ratio</div>
        <div className="font-semibold">72.4</div>
      </div>
      <div className="bg-gray-50 p-3 rounded-lg">
        <div className="text-xs text-gray-500 mb-1">Market Cap</div>
        <div className="font-semibold">$2.2T</div>
      </div>
    </div>
  );
};

export default MetricsPanel;
