from langchain_text_splitters import RecursiveCharacterTextSplitter
from schema.ragSchema import ChunkSchema
from schema.documentSchema import IngestionMetadataSchema
from constant.appConstants import MAX_CHUNK_SIZE, CHUNK_OVERLAP

def chunkText(rawText: str, metadata: IngestionMetadataSchema) -> list[ChunkSchema]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )

    rawChunks = splitter.split_text(rawText)

    chunks = []
    for i, chunkText in enumerate(rawChunks):
        if len(chunkText.strip()) < 50:
            continue

        chunk = ChunkSchema(
            text=chunkText.strip(),
            source=f"{metadata.company.value} {metadata.docType.value.upper()} {metadata.period}",
            section=f"chunk_{i}",
            company=metadata.company.value,
            docType=metadata.docType.value,
            date=metadata.period,
            namespace=metadata.namespace
        )
        chunks.append(chunk)

    return chunks
