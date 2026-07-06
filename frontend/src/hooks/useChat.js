// hooks/useChat.js
import { useState, useCallback, useRef } from "react";
import { useChatStore }    from "../store/chatStore";
import { useSessionStore } from "../store/sessionStore";
import { SOCKET_EVENTS }   from "../constants/SOCKET_EVENTS";
import { TYPING_DEBOUNCE_MS } from "../constants/APP_CONFIG";
import { getSocket }        from "./useSocket";

const useChat = () => {
  const [inputValue, setInputValue] = useState("");
  const typingTimeoutRef = useRef(null);

  const { isStreaming } = useChatStore();
  const { currentSession } = useSessionStore();

  const handleInputChange = useCallback((value) => {
    setInputValue(value);

    const socket = getSocket();
    if (!socket || !currentSession) return;

    // Emit typing_start immediately on first keystroke
    socket.emit(SOCKET_EVENTS.TYPING_START, { sessionId: currentSession.sessionId });

    // Emit typing_stop after TYPING_DEBOUNCE_MS of inactivity
    clearTimeout(typingTimeoutRef.current);
    typingTimeoutRef.current = setTimeout(() => {
      socket.emit(SOCKET_EVENTS.TYPING_STOP, { sessionId: currentSession.sessionId });
    }, TYPING_DEBOUNCE_MS);
  }, [currentSession]);

  const handleSendMessage = useCallback(() => {
    const question = inputValue.trim();
    if (!question || isStreaming || !currentSession) return;

    const socket = getSocket();
    if (!socket) return;

    const messageId = `msg_${Date.now()}`;

    socket.emit(SOCKET_EVENTS.ASK_QUESTION, {
      sessionId: currentSession.sessionId,
      question,
      messageId,
    });

    // Stop typing indicator immediately on send
    socket.emit(SOCKET_EVENTS.TYPING_STOP, { sessionId: currentSession.sessionId });
    clearTimeout(typingTimeoutRef.current);

    setInputValue("");
  }, [inputValue, isStreaming, currentSession]);

  return { inputValue, handleInputChange, handleSendMessage, isStreaming };
};

export default useChat;
