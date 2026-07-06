import { useEffect } from "react";
import { useParams, Navigate } from "react-router-dom";
import useSession from "../hooks/useSession";
import { useAuthStore } from "../store/authStore";
import { useSessionStore } from "../store/sessionStore";
import DashboardPage from "./DashboardPage";
import { FullPageSpinner } from "../components/common/Spinner";

const SessionPage = () => {
  const { id } = useParams();
  const { handleJoinSession } = useSession();
  const { isAuthenticated } = useAuthStore();
  const { currentSession } = useSessionStore();

  useEffect(() => {
    if (isAuthenticated && id && currentSession?.sessionId !== id) {
      handleJoinSession(id);
    }
  }, [id, isAuthenticated, handleJoinSession, currentSession]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (currentSession?.sessionId !== id) {
    return <FullPageSpinner />;
  }

  return <DashboardPage />;
};

export default SessionPage;
