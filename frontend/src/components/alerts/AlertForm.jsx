import React, { useState } from "react";
import useAlerts from "../../hooks/useAlerts";
import { SUPPORTED_TICKERS } from "../../constants/APP_CONFIG";

const AlertForm = () => {
  const { handleCreateAlert } = useAlerts();
  const [ticker, setTicker] = useState(SUPPORTED_TICKERS[0]);
  const [condition, setCondition] = useState("price_above");
  const [value, setValue] = useState("");

  const onSubmit = (e) => {
    e.preventDefault();
    if (!value || isNaN(value)) return;
    handleCreateAlert(ticker, condition, value);
    setValue("");
  };

  return (
    <div className="mb-6">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Set Price Alert</h3>
      <form onSubmit={onSubmit} className="flex flex-col space-y-3">
        <div className="flex space-x-2">
          <select
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="w-1/3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            {SUPPORTED_TICKERS.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          <select
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
            className="w-2/3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            <option value="price_above">Goes Above</option>
            <option value="price_below">Drops Below</option>
          </select>
        </div>
        <div className="flex space-x-2">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-500">$</div>
            <input
              type="number"
              step="0.01"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-7 p-2"
              placeholder="150.00"
              required
            />
          </div>
          <button
            type="submit"
            className="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-4 py-2 transition-colors"
          >
            Add
          </button>
        </div>
      </form>
    </div>
  );
};

export default AlertForm;
