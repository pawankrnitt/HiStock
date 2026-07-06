// services/reportService.js
import apiClient from "./apiClient";
import { API_ROUTES } from "../constants/API_ROUTES";

const triggerReport = async (sessionId) => {
  const response = await apiClient.post(API_ROUTES.REPORTS.TRIGGER(sessionId));
  return response.data;
};

const getReportUrl = async (sessionId) => {
  const response = await apiClient.get(API_ROUTES.REPORTS.GET(sessionId));
  return response.data;   // { status: "ready" | "pending", downloadUrl }
};

export { triggerReport, getReportUrl };
