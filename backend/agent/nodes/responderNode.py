import json
from agent.state import AgentState
from service.groqService import getCompletion, streamCompletion
from constant.appConstants import GROQ_MODEL_NAME
from socketio_layer.socketServer import sio
from enums.socketEventEnum import SocketEventEnum

RESPONDER_SYSTEM_PROMPT = """
You are a financial research assistant for NVIDIA (NVDA) and Tesla (TSLA) stocks.

STRICT RULES:
1. Answer ONLY using the provided context (document chunks, price data, news).
2. Do NOT use any prior training knowledge for specific financial figures, dates, or numbers.
3. After EVERY factual claim, include a citation: [Source: {document name}, {period}]
4. For price data, cite: [Source: Live Price Data, Alpha Vantage]
5. For news, cite: [Source: {article source}, {publishedAt}]
6. If the context is insufficient, say: "The available data does not contain enough information to answer this question accurately."
7. Never guess or invent numbers.
"""

def buildContextFromState(state: AgentState) -> str:
    """
    Build a comprehensive context string from all collected data in the agent state:
    - Document chunks (from search_documents tool calls)
    - Price data (from get_stock_price tool calls)
    - News articles (from search_news tool calls)
    - Ratio data (from calculate_ratio tool calls)
    """
    contextParts = []

    # Document chunks
    retrievedChunks = state.get("retrievedChunks", [])
    if retrievedChunks:
        contextParts.append("=== Financial Documents ===")
        for i, chunk in enumerate(retrievedChunks[:8], 1):    # top 8 chunks
            contextParts.append(
                f"[Doc {i}] Source: {chunk.get('source', 'Unknown')} | "
                f"Section: {chunk.get('section', '')}\n{chunk.get('text', '')}"
            )

    # Results from other tools (price, news, ratios)
    for result in state.get("subQueryResults", []):
        toolName    = result.get("tool")
        toolResult  = result.get("result", {})

        if toolName == "get_stock_price" and not toolResult.get("error"):
            contextParts.append(
                f"\n=== Price Data for {toolResult.get('ticker')} ===\n"
                f"Current Price: ${toolResult.get('currentPrice', 0):.2f} "
                f"({toolResult.get('changePercent', 0):+.2f}%)\n"
                f"[Source: Live Price Data, Alpha Vantage]"
            )

        elif toolName == "search_news" and not toolResult.get("error"):
            articles = toolResult.get("articles", [])
            if articles:
                contextParts.append("\n=== Recent News ===")
                for article in articles[:5]:    # top 5 articles
                    contextParts.append(
                        f"Title: {article.get('title', '')}\n"
                        f"Summary: {article.get('description', '')}\n"
                        f"[Source: {article.get('source', '')}, {article.get('publishedAt', '')}]"
                    )

        elif toolName == "calculate_ratio" and not toolResult.get("error"):
            contextParts.append(
                f"\n=== Financial Ratio: {toolResult.get('metric')} ===\n"
                f"{toolResult.get('ticker')}: {toolResult.get('value')} "
                f"(as of {toolResult.get('period', 'recent')})"
            )

    return "\n\n---\n\n".join(contextParts) if contextParts else "No context collected."

def buildSourcesFromState(state: AgentState) -> list[dict]:
    """Extract source references from all tool results for the response metadata."""
    sources = []

    # Sources from document chunks
    for chunk in state.get("retrievedChunks", [])[:5]:
        sources.append({
            "type":    "document",
            "doc":     chunk.get("source", ""),
            "section": chunk.get("section", ""),
            "company": chunk.get("company", ""),
            "date":    chunk.get("date", ""),
            "score":   chunk.get("score", 0.0)
        })

    # Sources from news
    for result in state.get("subQueryResults", []):
        if result.get("tool") == "search_news":
            for article in result.get("result", {}).get("articles", [])[:3]:
                sources.append({
                    "type":        "news",
                    "doc":         article.get("title", ""),
                    "section":     article.get("source", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "url":         article.get("url", "")
                })

    return sources

async def responderNode(state: AgentState) -> AgentState:
    """
    Generate the final cited answer.
    Phase 2: non-streaming (complete answer returned at once via REST).
    Phase 3: streams tokens via Socket.io when sessionId is present.
    """
    contextText = buildContextFromState(state)
    userPrompt  = f"Context:\n\n{contextText}\n\nQuestion: {state['question']}"
    sessionId   = state.get("sessionId", "")
    messageId   = state.get("messageId", "")    # passed through from questionHandler

    if sessionId:
        # ── STREAMING PATH (real-time, used by Socket.io question handler) ─────
        accumulatedAnswer = ""
        async for token in streamCompletion(
            systemPrompt=RESPONDER_SYSTEM_PROMPT,
            userPrompt=userPrompt,
            maxTokens=1500
        ):
            accumulatedAnswer += token
            await sio.emit(
                SocketEventEnum.AI_TOKEN,
                {"token": token, "messageId": messageId},
                room=sessionId
            )
        finalAnswer = accumulatedAnswer
    else:
        # ── NON-STREAMING PATH (Phase 2 REST /test/agent — unchanged behavior) ─
        finalAnswer = getCompletion(
            systemPrompt=RESPONDER_SYSTEM_PROMPT,
            userPrompt=userPrompt,
            maxTokens=1500
        )

    sources = buildSourcesFromState(state)

    return {
        **state,
        "finalAnswer": finalAnswer,
        "sources":     sources
    }

