// store/authStore.js
import { create } from "zustand";

export const useAuthStore = create((set) => ({
  accessToken:     null,
  refreshToken:    null,
  currentUser:     null,
  isAuthenticated: false,

  setTokens: (accessToken, refreshToken) =>
    set({ accessToken, refreshToken, isAuthenticated: true }),

  setCurrentUser: (user) => set({ currentUser: user }),

  logout: () => set({
    accessToken:     null,
    refreshToken:    null,
    currentUser:     null,
    isAuthenticated: false,
  }),
}));
