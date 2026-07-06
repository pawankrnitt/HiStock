// constants/APP_CONFIG.js

export const SUPPORTED_TICKERS    = ["NVDA", "TSLA"];
export const MAX_FILE_SIZE_MB     = 10;
export const MAX_FILE_SIZE_BYTES  = MAX_FILE_SIZE_MB * 1024 * 1024;
export const ALLOWED_FILE_TYPES   = ["application/pdf", "text/plain",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
export const ALLOWED_EXTENSIONS   = [".pdf", ".txt", ".docx"];
export const TYPING_DEBOUNCE_MS   = 1000;
export const PRICE_STALE_AFTER_MS = 15000;   // show stale indicator if no update
export const FREE_DAILY_LIMIT     = 10;
export const SOCKET_URL           = import.meta.env.VITE_SOCKET_URL;
export const API_BASE_URL         = import.meta.env.VITE_API_BASE_URL;
