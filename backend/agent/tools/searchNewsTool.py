from schema.agentSchema import SearchNewsInputSchema, SearchNewsOutputSchema
from service.newsService import searchNews

SEARCH_NEWS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_news",
        "description": "Search recent news articles and analyst coverage for NVDA or TSLA. Use for questions about recent events, analyst sentiment, ratings changes, or anything that happened in the last 30-90 days.",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "enum": ["NVDA", "TSLA"],
                    "description": "Company to search news for. Omit for both."
                },
                "daysBack": {
                    "type": "integer",
                    "description": "How many days back to search (1-90). Default 30.",
                    "default": 30
                }
            },
            "required": []
        }
    }
}

async def runSearchNewsTool(inputData: SearchNewsInputSchema) -> SearchNewsOutputSchema:
    """Run news search via NewsAPI."""
    try:
        companyStr = inputData.company.value if inputData.company else None
        return await searchNews(company=companyStr, daysBack=inputData.daysBack)

    except Exception as e:
        return SearchNewsOutputSchema(
            articles=[],
            totalResults=0,
            error=f"News search failed: {str(e)}"
        )
