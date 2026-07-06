// constants/SOCKET_EVENTS.js
export const SOCKET_EVENTS = {
  // Client → Server
  CREATE_SESSION:  "create_session",
  JOIN_SESSION:    "join_session",
  LEAVE_SESSION:   "leave_session",
  ASK_QUESTION:    "ask_question",
  TYPING_START:    "typing_start",
  TYPING_STOP:     "typing_stop",

  // Server → Client
  SESSION_CREATED:       "session_created",
  SESSION_JOINED:        "session_joined",
  USER_JOINED:           "user_joined",
  USER_LEFT:             "user_left",
  USER_TYPING:           "user_typing",
  USER_STOPPED_TYPING:   "user_stopped_typing",
  QUESTION_RECEIVED:     "question_received",
  AI_THINKING:           "ai_thinking",
  AI_TOKEN:              "ai_token",
  AI_DONE:               "ai_done",
  PRICE_UPDATE:          "price_update",
  ALERT_TRIGGERED:       "alert_triggered",
  DOCUMENT_PROCESSED:    "document_processed",
  REPORT_READY:          "report_ready",
  RATE_LIMIT_EXCEEDED:   "rate_limit_exceeded",
  ERROR:                 "error",
};
