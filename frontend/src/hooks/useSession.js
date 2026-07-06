// hooks/useSession.js
import { useState, useCallback } from "react";
import { createSession, getSessions, deleteSession } from "../services/sessionService";
import { useSessionStore } from "../store/sessionStore";
import { useChatStore }    from "../store/chatStore";
import { usePresenceStore } from "../store/presenceStore";
import { SOCKET_EVENTS }   from "../constants/SOCKET_EVENTS";
import { getSocket }        from "./useSocket";
import toast from "react-hot-toast";

const useSession = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { setSessions, addSession, clearCurrentSession } = useSessionStore();
  const { clearMessages } = useChatStore();
  const { clearPresence } = usePresenceStore();

  const loadSessions = useCallback(async () => {
    setIsLoading(true);
    try {
      const sessions = await getSessions();
      setSessions(sessions);
    } catch {
      toast.error("Failed to load sessions.");
    } finally {
      setIsLoading(false);
    }
  }, [setSessions]);

  const handleCreateSession = useCallback(async (name) => {
    setIsLoading(true);
    try {
      const newSession = await createSession(name);
      addSession(newSession);

      // Also emit socket event so backend joins the room immediately
      const socket = getSocket();
      socket?.emit(SOCKET_EVENTS.JOIN_SESSION, { sessionId: newSession.sessionId });

      return newSession;
    } catch {
      toast.error("Failed to create session.");
    } finally {
      setIsLoading(false);
    }
  }, [addSession]);

  const handleJoinSession = useCallback((sessionId) => {
    clearMessages();
    clearPresence();
    const socket = getSocket();
    socket?.emit(SOCKET_EVENTS.JOIN_SESSION, { sessionId });
  }, [clearMessages, clearPresence]);

  const handleLeaveSession = useCallback((sessionId) => {
    const socket = getSocket();
    socket?.emit(SOCKET_EVENTS.LEAVE_SESSION, { sessionId });
    clearCurrentSession();
    clearMessages();
    clearPresence();
  }, [clearCurrentSession, clearMessages, clearPresence]);

  const handleDeleteSession = useCallback(async (sessionId) => {
    try {
      await deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.sessionId !== sessionId));
      toast.success("Session deleted.");
    } catch {
      toast.error("Failed to delete session.");
    }
  }, [setSessions]);

  return {
    isLoading,
    loadSessions,
    handleCreateSession,
    handleJoinSession,
    handleLeaveSession,
    handleDeleteSession,
  };
};

export default useSession;
