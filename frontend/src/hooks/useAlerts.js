// hooks/useAlerts.js
import { useState, useCallback } from "react";
import { createAlert, getAlerts, deleteAlert } from "../services/alertService";
import toast from "react-hot-toast";

const useAlerts = () => {
  const [alerts, setAlerts]     = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const loadAlerts = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch {
      toast.error("Failed to load alerts.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleCreateAlert = useCallback(async (ticker, condition, value) => {
    try {
      const newAlert = await createAlert(ticker, condition, parseFloat(value));
      setAlerts((prev) => [newAlert, ...prev]);
      toast.success(`Alert set — ${ticker} ${condition === "price_below" ? "below" : "above"} $${value}`);
    } catch {
      toast.error("Failed to create alert.");
    }
  }, []);

  const handleDeleteAlert = useCallback(async (alertId) => {
    try {
      await deleteAlert(alertId);
      setAlerts((prev) => prev.filter((a) => a.alertId !== alertId));
      toast.success("Alert removed.");
    } catch {
      toast.error("Failed to remove alert.");
    }
  }, []);

  return { alerts, isLoading, loadAlerts, handleCreateAlert, handleDeleteAlert };
};

export default useAlerts;
