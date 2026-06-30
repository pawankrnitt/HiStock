from db.pineconeClient import getPineconeIndex
from rag.embedder import buildEmbedding
from schema.ragSchema import ChunkSchema, RetrievalResultSchema
from constant.appConstants import DEFAULT_TOP_K, PINECONE_PUBLIC_NAMESPACE

def retrieveChunks(
    query:     str,
    company:   str | None = None,
    userId:    str | None = None,
    topK:      int = DEFAULT_TOP_K
) -> RetrievalResultSchema:
    queryVector     = buildEmbedding(query)
    pineconeIndex   = getPineconeIndex()

    metadataFilter  = None
    if company:
        metadataFilter = {"company": {"$eq": company}}

    namespacesToSearch = [PINECONE_PUBLIC_NAMESPACE]
    if userId:
        namespacesToSearch.append(f"user_{userId}")

    allMatches = []
    for namespace in namespacesToSearch:
        result = pineconeIndex.query(
            vector=queryVector,
            top_k=topK,
            namespace=namespace,
            filter=metadataFilter,
            include_metadata=True
        )
        allMatches.extend(result.matches)

    allMatches.sort(key=lambda x: x.score, reverse=True)
    topMatches = allMatches[:topK]

    chunks = []
    for match in topMatches:
        meta = match.metadata
        chunks.append(ChunkSchema(
            text=meta.get("text", ""),
            source=meta.get("source", ""),
            section=meta.get("section", ""),
            company=meta.get("company", ""),
            docType=meta.get("docType", ""),
            date=meta.get("date", ""),
            namespace=meta.get("namespace", PINECONE_PUBLIC_NAMESPACE),
            score=match.score
        ))

    return RetrievalResultSchema(chunks=chunks, totalFound=len(allMatches))
