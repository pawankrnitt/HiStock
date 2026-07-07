// services/authService.js
import apiClient from "./apiClient";
import { API_ROUTES } from "../constants/API_ROUTES";

const signup = async (email, password, name) => {
  const response = await apiClient.post(API_ROUTES.AUTH.SIGNUP, { email, password, name, plan: "free" });
  return response.data;
};

const login = async (email, password) => {
  const response = await apiClient.post(API_ROUTES.AUTH.LOGIN, { email, password });
  return response.data;   // { accessToken, refreshToken, expiresIn }
};

const refresh = async (refreshToken) => {
  const response = await apiClient.post(API_ROUTES.AUTH.REFRESH, { refreshToken });
  return response.data;
};

export { signup, login, refresh };
