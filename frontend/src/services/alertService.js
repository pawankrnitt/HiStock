// services/alertService.js
import apiClient from "./apiClient";
import { API_ROUTES } from "../constants/API_ROUTES";

const createAlert = async (ticker, condition, value) => {
  const response = await apiClient.post(API_ROUTES.ALERTS.BASE, { ticker, condition, value });
  return response.data;
};

const getAlerts = async () => {
  const response = await apiClient.get(API_ROUTES.ALERTS.BASE);
  return response.data;
};

const deleteAlert = async (alertId) => {
  await apiClient.delete(API_ROUTES.ALERTS.BY_ID(alertId));
};

export { createAlert, getAlerts, deleteAlert };
