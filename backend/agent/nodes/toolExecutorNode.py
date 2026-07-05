import json
from datetime import datetime
from agent.state import AgentState
from schema.agentSchema import (
    StockPriceInputSchema, SearchDocumentsInputSchema,
    SearchNewsInputSchema, CalculateRatioInputSchema,
    ToolCallSchema
)
from agent.tools.stockPriceTool import runStockPriceTool
from agent.tools.searchDocumentsTool import runSearchDocumentsTool
from agent.tools.searchNewsTool import runSearchNewsTool
from agent.tools.calculateRatioTool import runCalculateRatioTool
from enums.toolNameEnum import ToolNameEnum
from socketio_layer.socketServer import sio
from enums.socketEventEnum import SocketEventEnum
from service.redisService import addTickersToSession

TOOL_DISPATCH = {
    ToolNameEnum.STOCK_PRICE:      (runStockPriceTool,       StockPriceInputSchema),
    ToolNameEnum.SEARCH_DOCUMENTS: (runSearchDocumentsTool,  SearchDocumentsInputSchema),
    ToolNameEnum.SEARCH_NEWS:      (runSearchNewsTool,       SearchNewsInputSchema),
    ToolNameEnum.CALCULATE_RATIO:  (runCalculateRatioTool,   CalculateRatioInputSchema),
}

# Friendly thinking-step labels shown to users while a tool runs
THINKING_LABELS = {
    ToolNameEnum.STOCK_PRICE:      "Fetching live price data...",
    ToolNameEnum.SEARCH_DOCUMENTS: "Searching financial documents...",
    ToolNameEnum.SEARCH_NEWS:      "Checking recent news...",
    ToolNameEnum.CALCULATE_RATIO:  "Calculating financial ratios...",
}

async def toolExecutorNode(state: AgentState) -> AgentState:
    """
    Execute all planned tool calls.
    Collects results into state["subQueryResults"] and state["retrievedChunks"].
    """
    # Get planned calls from last planning phase entry
    planningEntry = next(
        (entry for entry in reversed(state["toolCallHistory"]) if entry.get("phase") == "planning"),
        None
    )

    if not planningEntry:
        return state

    plannedCalls     = planningEntry.get("plannedCalls", [])
    newToolHistory   = list(state.get("toolCallHistory", []))
    subQueryResults  = list(state.get("subQueryResults", []))
    retrievedChunks  = list(state.get("retrievedChunks", []))
    mentionedTickers = set()

    for call in plannedCalls:
        toolName   = call.get("toolName")
        arguments  = call.get("arguments", {})

        if toolName not in TOOL_DISPATCH:
            continue

        # Emit a thinking step for this specific tool, if tied to a session
        if state.get("sessionId"):
            await sio.emit(
                SocketEventEnum.AI_THINKING,
                {"step": THINKING_LABELS.get(toolName, "Working on it...")},
                room=state["sessionId"]
            )

        toolFn, InputSchema = TOOL_DISPATCH[toolName]

        try:
            inputData   = InputSchema(**arguments)
            outputData  = await toolFn(inputData)
            outputDict  = outputData.model_dump()
            success     = not outputData.error if hasattr(outputData, 'error') else True

            # Track which ticker this call was about
            if "ticker" in arguments:
                mentionedTickers.add(arguments["ticker"])
            if "company" in arguments and arguments["company"]:
                mentionedTickers.add(arguments["company"])

        except Exception as e:
            outputDict = {"error": str(e)}
            success    = False

        # Record tool call in history
        toolCallRecord = ToolCallSchema(
            toolName=toolName,
            inputData=arguments,
            outputData=outputDict,
            success=success,
            calledAt=datetime.utcnow().isoformat()
        )
        newToolHistory.append(toolCallRecord.model_dump())
        subQueryResults.append({"tool": toolName, "result": outputDict})

        # Extract document chunks for context building
        if toolName == ToolNameEnum.SEARCH_DOCUMENTS and success:
            chunks = outputDict.get("chunks", [])
            retrievedChunks.extend(chunks)

    # Register mentioned tickers so the price ticker worker tracks this room
    if state.get("sessionId") and mentionedTickers:
        await addTickersToSession(state["sessionId"], list(mentionedTickers))

    return {
        **state,
        "toolCallHistory":  newToolHistory,
        "subQueryResults":  subQueryResults,
        "retrievedChunks":  retrievedChunks,
        "iterationCount":   state.get("iterationCount", 0) + 1
    }

