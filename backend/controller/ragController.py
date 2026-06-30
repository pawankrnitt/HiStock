from rag.retriever import retrieveChunks
from service.groqService import getCompletion
from schema.ragSchema import RagQuerySchema, RagResponseSchema, SourceSchema
from constant.appConstants import GROQ_MODEL_NAME, SUPPORTED_TICKERS

RAG_SYSTEM_PROMPT = """
You are a financial research assistant specializing in NVIDIA (NVDA) and Tesla (TSLA).
Answer ONLY using the document excerpts provided below as context.
Do NOT use any prior training knowledge for specific financial figures, dates, or numbers.
After every factual claim, include a citation in this exact format: [Source: {document name}, {period}]
If the provided context does not contain enough information to answer the question accurately, say:
"The available documents do not contain sufficient information to answer this question."
Never guess or invent financial data.
"""

def buildContextFromChunks(chunks: list) -> str:
    contextParts = []
    for i, chunk in enumerate(chunks, 1):
        contextParts.append(
            f"[Document {i}] Source: {chunk.source} | Section: {chunk.section}\n{chunk.text}"
        )
    return "\n\n---\n\n".join(contextParts)

async def testRagQuery(queryData: RagQuerySchema) -> RagResponseSchema:
    questionUpper = queryData.question.upper()
    isInScope     = any(ticker in questionUpper for ticker in SUPPORTED_TICKERS + ["NVIDIA", "TSLA"])

    if not isInScope:
        return RagResponseSchema(
            answer="This research assistant covers NVDA and TSLA only. Please ask about either of these stocks.",
            sources=[],
            model=GROQ_MODEL_NAME,
            question=queryData.question
        )

    companyFilter    = queryData.company.value if queryData.company else None
    retrievalResult  = retrieveChunks(
        query=queryData.question,
        company=companyFilter
    )

    if not retrievalResult.chunks:
        return RagResponseSchema(
            answer="No relevant documents found for this question. Please check if documents have been ingested.",
            sources=[],
            model=GROQ_MODEL_NAME,
            question=queryData.question
        )

    contextText  = buildContextFromChunks(retrievalResult.chunks)
    userPrompt   = f"Context Documents:\n\n{contextText}\n\nQuestion: {queryData.question}"

    answer = getCompletion(
        systemPrompt=RAG_SYSTEM_PROMPT,
        userPrompt=userPrompt
    )

    sources = [
        SourceSchema(
            doc=chunk.source,
            section=chunk.section,
            company=chunk.company,
            docType=chunk.docType,
            date=chunk.date,
            score=chunk.score or 0.0
        )
        for chunk in retrievalResult.chunks[:5]
    ]

    return RagResponseSchema(
        answer=answer,
        sources=sources,
        model=GROQ_MODEL_NAME,
        question=queryData.question
    )
