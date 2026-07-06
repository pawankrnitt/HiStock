// constants/API_ROUTES.js
const BASE = "/api/v1";

export const API_ROUTES = {
  AUTH: {
    SIGNUP:  `${BASE}/auth/signup`,
    LOGIN:   `${BASE}/auth/login`,
    REFRESH: `${BASE}/auth/refresh`,
  },
  SESSIONS: {
    BASE:      `${BASE}/sessions`,
    BY_ID:     (id) => `${BASE}/sessions/${id}`,
  },
  ALERTS: {
    BASE:      `${BASE}/alerts`,
    BY_ID:     (id) => `${BASE}/alerts/${id}`,
  },
  DOCUMENTS: {
    PRESIGN:   `${BASE}/documents/presign`,
    BASE:      `${BASE}/documents`,
    BY_ID:     (id) => `${BASE}/documents/${id}`,
  },
  REPORTS: {
    TRIGGER:   (id) => `${BASE}/reports/${id}`,
    GET:       (id) => `${BASE}/reports/${id}`,
  },
};
