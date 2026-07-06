// store/presenceStore.js
import { create } from "zustand";

export const usePresenceStore = create((set) => ({
  onlineMembers: [],    // [{ userId, name }]
  typingUsers:   [],    // [{ userId, name }]

  addMember: (member) =>
    set((state) => ({
      onlineMembers: state.onlineMembers.find((m) => m.userId === member.userId)
        ? state.onlineMembers
        : [...state.onlineMembers, member],
    })),

  removeMember: (userId) =>
    set((state) => ({
      onlineMembers: state.onlineMembers.filter((m) => m.userId !== userId),
      typingUsers:   state.typingUsers.filter((m) => m.userId !== userId),
    })),

  setTyping: (userId, name) =>
    set((state) => ({
      typingUsers: state.typingUsers.find((m) => m.userId === userId)
        ? state.typingUsers
        : [...state.typingUsers, { userId, name }],
    })),

  clearTyping: (userId) =>
    set((state) => ({
      typingUsers: state.typingUsers.filter((m) => m.userId !== userId),
    })),

  clearPresence: () => set({ onlineMembers: [], typingUsers: [] }),
}));
