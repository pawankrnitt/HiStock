// services/apiClient.js
import axios from "axios";
import { API_BASE_URL } from "../constants/APP_CONFIG";
import { useAuthStore } from "../store/authStore";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT from Zustand store to every outgoing request
apiClient.interceptors.request.use((config) => {
  const accessToken = useAuthStore.getState().accessToken;
  if (accessToken) {
    config.headers["Authorization"] = `Bearer ${accessToken}`;
  }
  return config;
});

// On 401, attempt one silent token refresh — if that also fails, log the user out
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retried) {
      originalRequest._retried = true;

      try {
        const { refreshToken, setTokens, logout } = useAuthStore.getState();
        const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, { refreshToken });
        const newAccessToken = response.data.accessToken;
        setTokens(newAccessToken, refreshToken);
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
      } catch {
        useAuthStore.getState().logout();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
