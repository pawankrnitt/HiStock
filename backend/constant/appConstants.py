# constant/appConstants.py
# ALL project constants live here — UPPER_SNAKE_CASE only
# Import from here everywhere else — never hardcode strings in other files

import os
from dotenv import load_dotenv

load_dotenv()

# ── Production config ──────────────────────────────────────────────────────────
# IS_PRODUCTION is True when running on ECS (ENVIRONMENT env var = "production")
# IS_PRODUCTION is False when running locally (default)
ENVIRONMENT       = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION     = ENVIRONMENT == "production"

ALLOWED_ORIGINS   = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

# ── AWS ──────────────────────────────────────────────────────────────────────
AWS_REGION                    = os.getenv("AWS_REGION", "ap-south-1")
S3_DOCUMENTS_BUCKET           = os.getenv("S3_DOCUMENTS_BUCKET", "histock-documents")

# ── DynamoDB Tables ──────────────────────────────────────────────────────────
DYNAMODB_PROCESSED_DOCS_TABLE = os.getenv("DYNAMODB_PROCESSED_DOCS_TABLE", "histock-processed-docs")
DYNAMODB_USERS_TABLE          = "histock-users"           # used from Phase 4
DYNAMODB_SESSIONS_TABLE       = "histock-sessions"        # used from Phase 3
DYNAMODB_MESSAGES_TABLE       = "histock-messages"        # used from Phase 3
DYNAMODB_ALERTS_TABLE         = "histock-alerts"          # used from Phase 4
DYNAMODB_USER_DOCS_TABLE      = "histock-user-documents"  # used from Phase 4

# ── Pinecone ──────────────────────────────────────────────────────────────────
PINECONE_API_KEY              = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME           = os.getenv("PINECONE_INDEX_NAME", "histock")
PINECONE_PUBLIC_NAMESPACE     = "public"

# ── Agent ────────────────────────────────────────────────────────────────────
MAX_AGENT_ITERATIONS       = 3       # max rounds of tool calls before forcing answer
MIN_CHUNKS_FOR_CONFIDENCE  = 2       # reflect node: at least this many chunks needed

# ── External API URLs ─────────────────────────────────────────────────────────
ALPHA_VANTAGE_BASE_URL     = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_KEY          = os.getenv("ALPHA_VANTAGE_KEY")
NEWS_API_BASE_URL          = "https://newsapi.org/v2/everything"
NEWS_API_KEY               = os.getenv("NEWS_API_KEY")
NEWS_API_SEARCH_FIELDS     = "title,description,content"

# ── News search company name map ──────────────────────────────────────────────
TICKER_TO_COMPANY_NAME     = {
    "NVDA": "NVIDIA",
    "TSLA": "Tesla"
}

# ── AI / ML ──────────────────────────────────────────────────────────────────
GROQ_API_KEY                  = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME               = "llama-3.3-70b-versatile"
EMBEDDING_MODEL_NAME          = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS          = 384

# ── RAG ──────────────────────────────────────────────────────────────────────
MAX_CHUNK_SIZE                = 500     # tokens
CHUNK_OVERLAP                 = 50      # tokens — overlap between adjacent chunks
DEFAULT_TOP_K                 = 8       # chunks to retrieve per query
MAX_AGENT_ITERATIONS          = 3       # used from Phase 2

# ── Stocks ────────────────────────────────────────────────────────────────────
SUPPORTED_TICKERS             = ["NVDA", "TSLA"]
SUPPORTED_COMPANY_NAMES       = ["NVIDIA", "TESLA", "NVDA", "TSLA"]

# ── External APIs ────────────────────────────────────────────────────────────
NEWS_API_KEY                  = os.getenv("NEWS_API_KEY")
ALPHA_VANTAGE_KEY             = os.getenv("ALPHA_VANTAGE_KEY")   # used from Phase 2

# ── Real-time (used from Phase 3) ────────────────────────────────────────────
UPSTASH_REDIS_URL             = os.getenv("UPSTASH_REDIS_URL")
SOCKET_REDIS_CHANNEL          = "stocksense_socketio"     # pub/sub channel name for Socket.io adapter
PRICE_POLL_INTERVAL_SECONDS   = 5
REDIS_PRICE_TTL               = 10      # seconds
REDIS_ACTIVE_SESSION_TTL      = 3600    # 1 hour
REDIS_SOCKET_MAP_TTL          = 3600    # 1 hour — socketId-to-userId mapping expiry

# ── Rate limiting (used from Phase 3) ────────────────────────────────────────
DAILY_FREE_QUERY_LIMIT        = 10
DAILY_PRO_QUERY_LIMIT         = 9999
RATE_LIMIT_KEY_PREFIX         = "ratelimit"

# ── Redis key prefixes (centralize all key naming — avoid typos across files) ─
REDIS_KEY_PRICE_CACHE         = "price"              # price:{ticker}
REDIS_KEY_ACTIVE_SESSIONS     = "active_sessions"     # single key — JSON list
REDIS_KEY_SOCKET_USER_MAP     = "socket"              # socket:{userId} → sid
REDIS_KEY_SESSION_TICKERS     = "session_tickers"     # session_tickers:{sessionId} → JSON list

# ── S3 Paths ──────────────────────────────────────────────────────────────────
S3_DOCUMENTS_PREFIX           = "documents"
S3_UPLOADS_PREFIX             = "user-uploads"
S3_REPORTS_PREFIX             = "reports"

# ── Cognito (add to existing appConstants.py) ──────────────────────────────────
COGNITO_USER_POOL_ID   = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID      = os.getenv("COGNITO_CLIENT_ID")
COGNITO_REGION         = os.getenv("AWS_REGION", "eu-north-1")
COGNITO_JWKS_URL       = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

# ── JWT ───────────────────────────────────────────────────────────────────────
JWT_ALGORITHM                = "RS256"
ACCESS_TOKEN_EXPIRY_SECONDS  = 3600         # 1 hour
REFRESH_TOKEN_EXPIRY_DAYS    = 30

# ── S3 — User uploads (extends Phase 1's S3 constants) ─────────────────────────
S3_UPLOADS_BUCKET            = os.getenv("S3_UPLOADS_BUCKET", "stocksense-uploads")
S3_REPORTS_BUCKET            = os.getenv("S3_REPORTS_BUCKET", "stocksense-reports")
PRESIGN_URL_EXPIRY_SECONDS   = 900          # 15 min to complete the upload
REPORT_URL_EXPIRY_SECONDS    = 86400        # 24 hours to download the report

# ── SQS (referenced here, actual queue + Lambda built in Phase 6) ──────────────
SQS_INGESTION_QUEUE_URL      = os.getenv("SQS_INGESTION_QUEUE_URL")

# ── Document upload limits ──────────────────────────────────────────────────────
MAX_UPLOAD_FILE_SIZE_MB      = 10
ALLOWED_UPLOAD_CONTENT_TYPES = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
