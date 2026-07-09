import { useEffect }        from "react";
import useSocket            from "../hooks/useSocket";
import useSession           from "../hooks/useSession";
import { useSessionStore }  from "../store/sessionStore";
import useAuth              from "../hooks/useAuth";

import SessionHeader   from "../components/session/SessionHeader";
import MemberList      from "../components/session/MemberList";
import TypingIndicator from "../components/session/TypingIndicator";
import MessageList     from "../components/chat/MessageList";
import ChatInput       from "../components/chat/ChatInput";
import ThinkingIndicator from "../components/chat/ThinkingIndicator";
import PriceChart      from "../components/dashboard/PriceChart";
import LiveTicker      from "../components/dashboard/LiveTicker";
import DocumentUpload  from "../components/upload/DocumentUpload";
import AlertForm       from "../components/alerts/AlertForm";
import AlertList       from "../components/alerts/AlertList";
import Button          from "../components/common/Button";
import ThemeToggle     from "../components/common/ThemeToggle";
import { LogOut }      from "lucide-react";

const DashboardPage = () => {
  useSocket();
  const { loadSessions, handleCreateSession } = useSession();
  const { sessions, currentSession } = useSessionStore();
  const { handleLogout } = useAuth();

  useEffect(() => { loadSessions(); }, [loadSessions]);

  return (
    <div className="h-screen flex bg-gray-50 dark:bg-gray-900 overflow-hidden">
      {/* ── Left sidebar — session list ─────────────────────────────────────── */}
      <aside className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex justify-between items-center mb-4">
            <h1 className="font-bold text-gray-900 dark:text-gray-100">HIStock</h1>
            <div className="flex gap-2">
              <ThemeToggle />
              <button onClick={handleLogout} className="p-2 text-gray-400 hover:text-red-500 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors" title="Logout">
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
          <Button onClick={() => handleCreateSession(`Session ${new Date().toLocaleDateString()}`)} className="w-full text-sm">
            + New Session
          </Button>
        </div>
        <nav className="flex-1 overflow-y-auto p-2 space-y-1">
          {sessions.map((session) => (
            <SessionListItem key={session.sessionId} session={session} />
          ))}
        </nav>
      </aside>

      {/* ── Main chat area ───────────────────────────────────────────────────── */}
      <main className="flex-1 flex flex-col min-w-0 bg-white dark:bg-gray-800">
        {currentSession ? (
          <>
            <SessionHeader session={currentSession} />
            <div className="flex-1 overflow-y-auto bg-gray-50/50 dark:bg-gray-900/50">
              <MessageList />
            </div>
            <ThinkingIndicator />
            <TypingIndicator />
            <ChatInput />
          </>
        ) : (
          <EmptyState />
        )}
      </main>

      {/* ── Right sidebar — chart, prices, upload, alerts ───────────────────── */}
      <aside className="w-80 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col overflow-y-auto">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <LiveTicker ticker="NVDA" />
          <LiveTicker ticker="TSLA" />
        </div>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <PriceChart />
        </div>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <MemberList />
        </div>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-900/30">
          <DocumentUpload />
        </div>
        <div className="p-4">
          <AlertForm />
          <AlertList />
        </div>
      </aside>
    </div>
  );
};

const SessionListItem = ({ session }) => {
  const { handleJoinSession } = useSession();
  const { currentSession }    = useSessionStore();
  const isActive = currentSession?.sessionId === session.sessionId;

  return (
    <button
      onClick={() => handleJoinSession(session.sessionId)}
      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
        isActive ? "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-medium" : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
      }`}
    >
      <div className="font-medium truncate">{session.name}</div>
      <div className="text-[10px] text-gray-400">ID: {session.sessionId.split("_")[1]}</div>
    </button>
  );
};

const EmptyState = () => (
  <div className="flex-1 flex items-center justify-center text-center px-8">
    <div>
      <p className="text-4xl mb-4">📊</p>
      <p className="text-gray-700 dark:text-gray-300 font-medium text-lg">Welcome to HIStock</p>
      <p className="text-gray-500 dark:text-gray-400 mt-2 max-w-sm">Select a session from the left to start researching NVDA or TSLA, or create a new session to begin.</p>
    </div>
  </div>
);

export default DashboardPage;
