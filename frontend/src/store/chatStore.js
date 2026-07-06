// store/chatStore.js
import { create } from "zustand";

export const useChatStore = create((set) => ({
  messages:      [],     // list of { messageId, question, answer, sources, isStreaming, askedBy }
  thinkingStep:  null,   // "Searching documents..." | null
  isStreaming:   false,

  addMessage: (message) =>
    set((state) => ({
      messages:  [...state.messages, message],
      isStreaming: message.isStreaming ?? false,
    })),

  appendToken: (messageId, token) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.messageId === messageId
          ? { ...m, answer: m.answer + token, isStreaming: true }
          : m
      ),
    })),

  finalizeMessage: (messageId, fullAnswer, sources) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.messageId === messageId
          ? { ...m, answer: fullAnswer, sources, isStreaming: false }
          : m
      ),
      isStreaming: false,
    })),

  setThinkingStep: (step) => set({ thinkingStep: step }),

  clearMessages: () => set({ messages: [], thinkingStep: null, isStreaming: false }),
}));
