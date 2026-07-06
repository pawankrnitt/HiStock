// services/sessionService.js
import apiClient from "./apiClient";
import { API_ROUTES } from "../constants/API_ROUTES";

const createSession = async (name) => {
  const response = await apiClient.post(API_ROUTES.SESSIONS.BASE, { name });
  return response.data;
};

const getSessions = async () => {
  const response = await apiClient.get(API_ROUTES.SESSIONS.BASE);
  return response.data;
};

const getSession = async (sessionId) => {
  const response = await apiClient.get(API_ROUTES.SESSIONS.BY_ID(sessionId));
  return response.data;
};

const deleteSession = async (sessionId) => {
  await apiClient.delete(API_ROUTES.SESSIONS.BY_ID(sessionId));
};

export { createSession, getSessions, getSession, deleteSession };
