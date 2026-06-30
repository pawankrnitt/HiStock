from agent.state import AgentState
from constant.appConstants import MAX_AGENT_ITERATIONS, MIN_CHUNKS_FOR_CONFIDENCE

async def reflectNode(state: AgentState) -> AgentState:
    """
    Reflection logic:
      1. If max iterations reached → force answer (avoid infinite loop)
      2. If enough document chunks retrieved → answer
      3. If any tool call returned an error on all attempts → answer anyway
      4. Otherwise → loop back to toolExecutor for more context

    Why a hard iteration limit?
    The agent could theoretically loop forever if it never feels "confident".
    MAX_AGENT_ITERATIONS prevents runaway LLM cost and latency.
    """
    iterationCount   = state.get("iterationCount", 0)
    retrievedChunks  = state.get("retrievedChunks", [])
    subQueryResults  = state.get("subQueryResults", [])

    # Rule 1: Hard stop — max iterations reached
    if iterationCount >= MAX_AGENT_ITERATIONS:
        return {**state, "hasEnoughContext": True}

    # Rule 2: Good chunk coverage — at least MIN_CHUNKS_FOR_CONFIDENCE chunks
    hasGoodChunkCoverage = len(retrievedChunks) >= MIN_CHUNKS_FOR_CONFIDENCE

    # Rule 3: Check if news was fetched (for questions about recent events)
    hasNewsData = any(r.get("tool") == "search_news" for r in subQueryResults)

    # Rule 4: Check if price data was fetched (for price questions)
    hasPriceData = any(r.get("tool") == "get_stock_price" for r in subQueryResults)

    # If we have chunks — assume we have enough for a grounded answer
    hasEnoughContext = hasGoodChunkCoverage

    return {**state, "hasEnoughContext": hasEnoughContext}

def shouldContinue(state: AgentState) -> str:
    """
    LangGraph conditional edge function.
    Called after reflectNode to decide next node.
    Returns "continue" (→ toolExecutor) or "end" (→ responder).
    """
    if state.get("hasEnoughContext", False):
        return "end"
    return "continue"
