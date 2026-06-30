from agent.graph import agentGraph
from schema.agentSchema import AgentQuerySchema, AgentResponseSchema, ToolCallSchema
from constant.appConstants import GROQ_MODEL_NAME, SUPPORTED_TICKERS, SUPPORTED_COMPANY_NAMES

OUT_OF_SCOPE_MESSAGE = (
    "This research assistant covers NVDA (NVIDIA) and TSLA (Tesla) only. "
    "Please ask a question about either of these stocks."
)

def isQueryInScope(question: str) -> bool:
    questionUpper  = question.upper()
    allKnownNames  = SUPPORTED_TICKERS + [n.upper() for n in SUPPORTED_COMPANY_NAMES]
    return any(name in questionUpper for name in allKnownNames)

async def runAgentQuery(queryData: AgentQuerySchema) -> AgentResponseSchema:
    """
    Run the full agentic pipeline for a user question.
    Returns grounded cited answer with tool call trace.
    """
    if not isQueryInScope(queryData.question):
        return AgentResponseSchema(
            answer=OUT_OF_SCOPE_MESSAGE,
            sources=[],
            toolCallHistory=[],
            iterationCount=0,
            model=GROQ_MODEL_NAME,
            question=queryData.question
        )

    # Build initial agent state
    initialState = {
        "question":         queryData.question,
        "sessionId":        queryData.sessionId or "",
        "userId":           "",
        "company":          queryData.company.value if queryData.company else "both",
        "planSteps":        [],
        "toolCallHistory":  [],
        "subQueryResults":  [],
        "retrievedChunks":  [],
        "hasEnoughContext": False,
        "iterationCount":   0,
        "finalAnswer":      None,
        "sources":          []
    }

    # Run LangGraph agent — synchronous in Phase 2
    finalState = await agentGraph.ainvoke(initialState)

    # Build tool call history for response
    toolCallHistory = [
        ToolCallSchema(**record)
        for record in finalState.get("toolCallHistory", [])
        if isinstance(record, dict) and "toolName" in record
    ]

    return AgentResponseSchema(
        answer=finalState.get("finalAnswer") or "Unable to generate an answer with available context.",
        sources=finalState.get("sources", []),
        toolCallHistory=toolCallHistory,
        iterationCount=finalState.get("iterationCount", 0),
        model=GROQ_MODEL_NAME,
        question=queryData.question
    )
