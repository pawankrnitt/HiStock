from groq import Groq
from constant.appConstants import GROQ_API_KEY, GROQ_MODEL_NAME

_groqClient = None

def getGroqClient() -> Groq:
    global _groqClient
    if _groqClient is None:
        _groqClient = Groq(api_key=GROQ_API_KEY)
    return _groqClient

def getCompletion(
    systemPrompt: str,
    userPrompt:   str,
    maxTokens:    int = 1024
) -> str:
    """Non-streaming completion — used in Phase 1 test endpoint and Phase 6 report generator."""
    client   = getGroqClient()
    response = client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user",   "content": userPrompt}
        ],
        max_tokens=maxTokens,
        temperature=0.1
    )
    return response.choices[0].message.content

async def streamCompletion(
    systemPrompt: str,
    userPrompt:   str,
    maxTokens:    int = 1024
):
    """
    Streaming completion — yields one token at a time.
    Used from Phase 3 onwards inside responderNode when Socket.io is available.
    The caller (Socket.io handler) emits each token as an "ai_token" event.
    """
    client = getGroqClient()
    stream = client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user",   "content": userPrompt}
        ],
        max_tokens=maxTokens,
        temperature=0.1,
        stream=True
    )

    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token

def getCompletionWithToolCalling(
    systemPrompt: str,
    userPrompt:   str,
    tools:        list[dict]
) -> dict:
    """
    Completion with tool calling enabled.
    Used in plannerNode to let LLM decide which tools to call.
    Returns raw response dict — plannerNode parses the tool_calls.
    """
    client   = getGroqClient()
    response = client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user",   "content": userPrompt}
        ],
        tools=tools,
        tool_choice="auto",
        temperature=0.1
    )
    return response.choices[0].message
