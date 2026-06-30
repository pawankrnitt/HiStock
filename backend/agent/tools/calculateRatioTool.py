from schema.agentSchema import CalculateRatioInputSchema, RatioOutputSchema
from enums.tickerEnum import TickerEnum

CALCULATE_RATIO_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "calculate_ratio",
        "description": "Calculate key financial ratios for NVDA or TSLA such as P/E ratio, gross margin, or debt-to-equity. Use when the question asks about valuation or financial efficiency metrics.",
        "parameters": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": ["pe_ratio", "gross_margin", "debt_to_equity", "revenue_growth", "operating_margin"],
                    "description": "The financial ratio to calculate"
                },
                "ticker": {
                    "type": "string",
                    "enum": ["NVDA", "TSLA"],
                    "description": "The stock ticker"
                }
            },
            "required": ["metric", "ticker"]
        }
    }
}

# Demo data — replace with real API call in production
DEMO_RATIOS = {
    "NVDA": {
        "pe_ratio":        68.2,
        "gross_margin":    74.6,
        "debt_to_equity":  0.42,
        "revenue_growth":  122.0,
        "operating_margin": 61.9
    },
    "TSLA": {
        "pe_ratio":        52.1,
        "gross_margin":    17.9,
        "debt_to_equity":  0.08,
        "revenue_growth":  8.7,
        "operating_margin": 8.2
    }
}

async def runCalculateRatioTool(inputData: CalculateRatioInputSchema) -> RatioOutputSchema:
    """Calculate or look up a financial ratio for the given ticker."""
    try:
        tickerRatios = DEMO_RATIOS.get(inputData.ticker.value, {})
        value        = tickerRatios.get(inputData.metric)

        return RatioOutputSchema(
            metric=inputData.metric,
            ticker=inputData.ticker.value,
            value=value,
            period="Q3 FY2024"
        )
    except Exception as e:
        return RatioOutputSchema(
            metric=inputData.metric,
            ticker=inputData.ticker.value,
            value=None,
            error=str(e)
        )
