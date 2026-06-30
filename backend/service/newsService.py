import httpx
from datetime import datetime, timedelta
from schema.agentSchema import SearchNewsOutputSchema, NewsArticleSchema
from constant.appConstants import NEWS_API_BASE_URL, NEWS_API_KEY, TICKER_TO_COMPANY_NAME

async def searchNews(company: str | None, daysBack: int = 30) -> SearchNewsOutputSchema:
    """
    Search NewsAPI for recent articles about NVDA or TSLA.

    company: "NVDA" | "TSLA" | None (search both)
    daysBack: how many days back to search (1-90)

    Free tier: 100 requests/day, results up to 30 days old.
    """
    fromDate = (datetime.utcnow() - timedelta(days=daysBack)).strftime("%Y-%m-%d")

    # Build search query from ticker → company name map
    if company:
        companyName = TICKER_TO_COMPANY_NAME.get(company, company)
        searchQuery = f"{companyName} OR {company} stock earnings revenue"
    else:
        searchQuery = "NVIDIA NVDA Tesla TSLA stock earnings"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(NEWS_API_BASE_URL, params={
            "q":        searchQuery,
            "from":     fromDate,
            "sortBy":   "relevancy",
            "language": "en",
            "pageSize": 10,
            "apiKey":   NEWS_API_KEY
        })
        response.raise_for_status()
        data = response.json()

    if data.get("status") != "ok":
        return SearchNewsOutputSchema(
            articles=[],
            totalResults=0,
            error=data.get("message", "NewsAPI error")
        )

    articles = []
    for article in data.get("articles", []):
        articles.append(NewsArticleSchema(
            title=article.get("title", ""),
            description=article.get("description"),
            source=article.get("source", {}).get("name", "Unknown"),
            publishedAt=article.get("publishedAt", ""),
            url=article.get("url", "")
        ))

    return SearchNewsOutputSchema(
        articles=articles,
        totalResults=data.get("totalResults", 0)
    )
