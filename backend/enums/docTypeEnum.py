from enum import Enum

class DocTypeEnum(str, Enum):
    TEN_K               = "ten_k"
    TEN_Q               = "ten_q"
    EARNINGS_TRANSCRIPT = "earnings_transcript"
    NEWS_SUMMARY        = "news_summary"
    USER_UPLOAD         = "user_upload"
