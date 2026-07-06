import React, { useEffect } from "react";
import useAlerts from "../../hooks/useAlerts";
import { Trash2, BellRing } from "lucide-react";
import { formatCurrency } from "../../utils/formatCurrency";
import Spinner from "../common/Spinner";

const AlertList = () => {
  const { alerts, isLoading, loadAlerts, handleDeleteAlert } = useAlerts();

  useEffect(() => {
    loadAlerts();
  }, [loadAlerts]);

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
        <BellRing className="w-4 h-4 mr-2 text-gray-500" />
        Active Alerts
      </h3>
      
      {isLoading ? (
        <div className="flex justify-center p-4"><Spinner size="sm" /></div>
      ) : alerts.length === 0 ? (
        <p className="text-sm text-gray-500 italic">No active alerts.</p>
      ) : (
        <ul className="space-y-2">
          {alerts.map((alert) => (
            <li key={alert.alertId} className="flex justify-between items-center bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div className="flex flex-col">
                <span className="text-sm font-bold text-gray-900">{alert.ticker}</span>
                <span className="text-xs text-gray-600">
                  {alert.condition === "price_above" ? "above" : "below"}{" "}
                  <span className="font-semibold">{formatCurrency(alert.value)}</span>
                </span>
              </div>
              <button
                onClick={() => handleDeleteAlert(alert.alertId)}
                className="text-gray-400 hover:text-red-500 transition-colors p-1 rounded-md hover:bg-red-50"
                title="Delete Alert"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AlertList;
