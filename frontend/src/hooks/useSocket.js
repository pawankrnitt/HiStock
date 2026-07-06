// hooks/useSocket.js
import { useEffect, useCallback } from "react";
import { io } from "socket.io-client";
import { SOCKET_URL } from "../constants/APP_CONFIG";
import { SOCKET_EVENTS } from "../constants/SOCKET_EVENTS";
import { useAuthStore }     from "../store/authStore";
import { useChatStore }     from "../store/chatStore";
import { usePresenceStore } from "../store/presenceStore";
import { usePriceStore }    from "../store/priceStore";
import { useSessionStore }  from "../store/sessionStore";

const socketRef = { current: null };

export const getSocket = () => socketRef.current;

const useSocket = () => {
  const { accessToken, isAuthenticated } = useAuthStore();
  const {
    appendToken, setThinkingStep, finalizeMessage, addMessage
  } = useChatStore();
  const { addMember, removeMember, setTyping, clearTyping } = usePresenceStore();
  const { updatePrice }    = usePriceStore();
  const { setCurrentSession } = useSessionStore();

  const connectSocket = useCallback(() => {
    if (socketRef.current?.connected) return;

    socketRef.current = io(SOCKET_URL, {
      auth:              { token: accessToken },
      transports:        ["websocket"],
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    const sio = socketRef.current;

    sio.on("connect", () => console.log("[socket] connected:", sio.id));
    sio.on("disconnect", () => console.log("[socket] disconnected"));
    sio.on("connect_error", (err) => console.error("[socket] connect error:", err.message));

    // ── Session events ────────────────────────────────────────────────────────
    sio.on(SOCKET_EVENTS.SESSION_JOINED, ({ sessionId, history, members }) => {
      setCurrentSession({ sessionId, members });
      history.forEach((msg) => addMessage(msg));
    });

    sio.on(SOCKET_EVENTS.USER_JOINED, ({ userId, name }) => addMember({ userId, name }));
    sio.on(SOCKET_EVENTS.USER_LEFT,   ({ userId })       => removeMember(userId));

    // ── Presence ──────────────────────────────────────────────────────────────
    sio.on(SOCKET_EVENTS.USER_TYPING,          ({ userId, name }) => setTyping(userId, name));
    sio.on(SOCKET_EVENTS.USER_STOPPED_TYPING,  ({ userId })       => clearTyping(userId));

    // ── AI streaming ─────────────────────────────────────────────────────────
    sio.on(SOCKET_EVENTS.QUESTION_RECEIVED, ({ question, askedBy, messageId }) => {
      addMessage({ messageId, question, answer: "", sources: [], isStreaming: true, askedBy });
    });

    sio.on(SOCKET_EVENTS.AI_THINKING, ({ step }) => setThinkingStep(step));

    sio.on(SOCKET_EVENTS.AI_TOKEN, ({ token, messageId }) => appendToken(messageId, token));

    sio.on(SOCKET_EVENTS.AI_DONE, ({ messageId, answer, sources }) => {
      finalizeMessage(messageId, answer, sources);
      setThinkingStep(null);
    });

    // ── Live prices ───────────────────────────────────────────────────────────
    sio.on(SOCKET_EVENTS.PRICE_UPDATE, ({ ticker, price, change, changePercent }) => {
      updatePrice(ticker, { price, change, changePercent, updatedAt: Date.now() });
    });

    // ── Notifications ─────────────────────────────────────────────────────────
    sio.on(SOCKET_EVENTS.DOCUMENT_PROCESSED, ({ docId, fileName }) => {
      import("react-hot-toast").then(({ default: toast }) =>
        toast.success(`"${fileName}" is ready — you can now ask questions about it.`)
      );
    });

    sio.on(SOCKET_EVENTS.REPORT_READY, ({ downloadUrl }) => {
      import("react-hot-toast").then(({ default: toast }) =>
        toast.success("Report ready!", {
          duration: 8000,
          action: { label: "Download", onClick: () => window.open(downloadUrl, "_blank") }
        })
      );
    });

    sio.on(SOCKET_EVENTS.ALERT_TRIGGERED, ({ ticker, condition, value, currentPrice }) => {
      import("react-hot-toast").then(({ default: toast }) =>
        toast(`🔔 ${ticker} alert: price ${condition === "price_below" ? "below" : "above"} $${value} (now $${currentPrice})`, {
          duration: 10000
        })
      );
    });

    sio.on(SOCKET_EVENTS.RATE_LIMIT_EXCEEDED, ({ message }) => {
      import("react-hot-toast").then(({ default: toast }) => toast.error(message));
    });

    sio.on(SOCKET_EVENTS.ERROR, ({ code, message }) => {
      console.error("[socket error]", code, message);
    });
  }, [accessToken]);

  const disconnectSocket = useCallback(() => {
    socketRef.current?.disconnect();
    socketRef.current = null;
  }, []);

  useEffect(() => {
    if (isAuthenticated && accessToken) {
      connectSocket();
    } else {
      disconnectSocket();
    }
    return () => { /* intentionally no cleanup — singleton persists across renders */ };
  }, [isAuthenticated, accessToken, connectSocket, disconnectSocket]);

  const emitEvent = useCallback((event, data) => {
    socketRef.current?.emit(event, data);
  }, []);

  return { emitEvent, isConnected: !!socketRef.current?.connected };
};

export default useSocket;
