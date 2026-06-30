from schema.agentSchema import SearchDocumentsInputSchema, SearchDocumentsOutputSchema
from rag.retriever import retrieveChunks

SEARCH_DOCUMENTS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search ingested financial documents (SEC filings, earnings transcripts) for NVDA or TSLA. Use for questions about revenue, earnings, guidance, financial metrics, management commentary, risk factors.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Specific search query — be precise, e.g. 'NVDA data center revenue Q3 2024'"
                },
                "company": {
                    "type": "string",
                    "enum": ["NVDA", "TSLA"],
                    "description": "Filter to a specific company. Omit to search both."
                }
            },
            "required": ["query"]
        }
    }
}

async def runSearchDocumentsTool(inputData: SearchDocumentsInputSchema) -> SearchDocumentsOutputSchema:
    """
    Run semantic search over Pinecone.
    Returns top-K chunks relevant to the query.
    """
    try:
        companyFilter  = inputData.company.value if inputData.company else None
        retrievalResult = retrieveChunks(
            query=inputData.query,
            company=companyFilter
        )

        return SearchDocumentsOutputSchema(
            chunks=[chunk.model_dump() for chunk in retrievalResult.chunks],
            totalFound=retrievalResult.totalFound
        )

    except Exception as e:
        return SearchDocumentsOutputSchema(
            chunks=[],
            totalFound=0,
            error=f"Document search failed: {str(e)}"
        )
