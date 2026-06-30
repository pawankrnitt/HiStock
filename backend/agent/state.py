from typing import TypedDict

class AgentState(TypedDict):
    # Input
    question:         str
    sessionId:        str       # empty string in Phase 2 — used from Phase 3
    userId:           str       # empty string in Phase 2 — used from Phase 4
    company:          str       # "NVDA" | "TSLA" | "both" | ""

    # Planning
    planSteps:        list[str]

    # Execution
    toolCallHistory:  list[dict]    # list of ToolCallSchema dicts
    subQueryResults:  list[dict]    # list of {tool, result} dicts
    retrievedChunks:  list[dict]    # list of ChunkSchema dicts from search_documents

    # Reflection
    hasEnoughContext: bool
    iterationCount:   int

    # Output
    finalAnswer:      str | None
    sources:          list[dict]
