import json
from agent.state import AgentState
from service.groqService import getCompletionWithToolCalling
from agent.tools.stockPriceTool import STOCK_PRICE_TOOL_DEFINITION
from agent.tools.searchDocumentsTool import SEARCH_DOCUMENTS_TOOL_DEFINITION
from agent.tools.searchNewsTool import SEARCH_NEWS_TOOL_DEFINITION
from agent.tools.calculateRatioTool import CALCULATE_RATIO_TOOL_DEFINITION

ALL_TOOL_DEFINITIONS = [
    STOCK_PRICE_TOOL_DEFINITION,
    SEARCH_DOCUMENTS_TOOL_DEFINITION,
    SEARCH_NEWS_TOOL_DEFINITION,
    CALCULATE_RATIO_TOOL_DEFINITION
]

PLANNER_SYSTEM_PROMPT = """
You are a financial research planner for NVDA and TSLA stocks.
Given a user question, decide which tools to call to gather the necessary information.
You have access to: get_stock_price, search_documents, search_news, calculate_ratio.

Guidelines:
- For questions about financials, earnings, guidance → use search_documents
- For questions about current/historical price → use get_stock_price
- For questions about recent events, analyst opinions → use search_news
- For questions about valuation ratios → use calculate_ratio
- For comparison questions → call tools for each company separately
- You may call multiple tools — call all that are needed

IMPORTANT: Only call tools for NVDA or TSLA. Reject anything else.
"""

async def plannerNode(state: AgentState) -> AgentState:
    """
    Planning node — uses LLM tool calling to decide which tools to invoke.
    Stores planned tool calls in state["planSteps"].
    """
    responseMessage = getCompletionWithToolCalling(
        systemPrompt=PLANNER_SYSTEM_PROMPT,
        userPrompt=f"Question: {state['question']}",
        tools=ALL_TOOL_DEFINITIONS
    )

    # Parse tool calls from LLM response
    plannedCalls = []
    if hasattr(responseMessage, "tool_calls") and responseMessage.tool_calls:
        for toolCall in responseMessage.tool_calls:
            plannedCalls.append({
                "toolName":  toolCall.function.name,
                "arguments": json.loads(toolCall.function.arguments)
            })

    # If LLM decided no tools are needed (simple question) — go straight to responder
    if not plannedCalls:
        plannedCalls = [{
            "toolName":  "search_documents",
            "arguments": {"query": state["question"]}
        }]

    return {
        **state,
        "planSteps": [str(call) for call in plannedCalls],
        "toolCallHistory": state.get("toolCallHistory", []) + [
            {"phase": "planning", "plannedCalls": plannedCalls}
        ]
    }
