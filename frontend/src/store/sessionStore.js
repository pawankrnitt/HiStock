// store/sessionStore.js
import { create } from "zustand";

export const useSessionStore = create((set) => ({
  sessions:       [],
  currentSession: null,

  setSessions: (sessions)         => set({ sessions }),
  setCurrentSession: (session)    => set({ currentSession: session }),
  addSession: (session)           => set((s) => ({ sessions: [session, ...s.sessions] })),
  clearCurrentSession: ()         => set({ currentSession: null }),
}));
