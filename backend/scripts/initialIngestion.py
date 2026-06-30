import asyncio
import hashlib
import io
from datetime import datetime

import httpx
import pdfplumber
from bs4 import BeautifulSoup

from rag.chunker import chunkText
from rag.embedder import buildEmbeddingsBatch
from repo.processedDocRepo import docAlreadyProcessed, insertProcessedDoc
from service.s3Service import uploadRawDocument
from db.pineconeClient import getPineconeIndex
from schema.documentSchema import IngestionMetadataSchema, ProcessedDocSchema
from enums.tickerEnum import TickerEnum
from enums.docTypeEnum import DocTypeEnum
from constant.appConstants import (
    S3_DOCUMENTS_PREFIX,
    PINECONE_PUBLIC_NAMESPACE,
)

DOCUMENTS_TO_INGEST = [
    {
        "company":  TickerEnum.NVDA,
        "docType":  DocTypeEnum.TEN_K,
        "period":   "FY2024",
        "url":      "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000029/nvda-20240128.htm",
    },
    {
        "company":  TickerEnum.NVDA,
        "docType":  DocTypeEnum.TEN_K,
        "period":   "FY2023",
        "url":      "https://www.sec.gov/Archives/edgar/data/1045810/000104581023000017/nvda-20230129.htm",
    }
]

def generateDocId(company: str, docType: str, period: str) -> str:
    rawString = f"{company}-{docType}-{period}"
    return hashlib.md5(rawString.encode()).hexdigest()[:12]

async def downloadDocumentBytes(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        response = await client.get(url, headers={
            "User-Agent": "HiStock Research Bot contact@histock.ai"
        })
        response.raise_for_status()
        return response.content

def extractTextFromBytes(fileBytes: bytes, url: str) -> str:
    """Extract plain text from either PDF or HTML bytes depending on the URL."""
    if url.lower().endswith('.htm') or url.lower().endswith('.html'):
        # Parse HTML for SEC EDGAR filings
        soup = BeautifulSoup(fileBytes, 'lxml')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        rawText = soup.get_text(separator='\n')
    else:
        # Parse PDF using pdfplumber
        rawText = ""
        try:
            with pdfplumber.open(io.BytesIO(fileBytes)) as pdf:
                for page in pdf.pages:
                    pageText = page.extract_text()
                    if pageText:
                        rawText += pageText + "\n\n"
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {e}")

    lines      = rawText.split("\n")
    cleanLines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleanLines)

def upsertToPinecone(
    chunks:     list,
    embeddings: list[list[float]],
    namespace:  str
) -> int:
    pineconeIndex = getPineconeIndex()

    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectorId = f"{chunk.company}_{chunk.docType}_{chunk.date}_{i}"
        vectors.append({
            "id":     vectorId,
            "values": embedding,
            "metadata": {
                "text":      chunk.text,
                "source":    chunk.source,
                "section":   chunk.section,
                "company":   chunk.company,
                "docType":   chunk.docType,
                "date":      chunk.date,
                "namespace": chunk.namespace,
            }
        })

    UPSERT_BATCH_SIZE = 100
    for batchStart in range(0, len(vectors), UPSERT_BATCH_SIZE):
        batch = vectors[batchStart : batchStart + UPSERT_BATCH_SIZE]
        pineconeIndex.upsert(vectors=batch, namespace=namespace)

    return len(vectors)

async def ingestDocument(docConfig: dict) -> None:
    company  = docConfig["company"]
    docType  = docConfig["docType"]
    period   = docConfig["period"]
    url      = docConfig["url"]
    docId    = generateDocId(company.value, docType.value, period)

    if docAlreadyProcessed(docId):
        print(f"  [SKIP] Already processed: {company.value} {docType.value} {period}")
        return

    print(f"  [START] {company.value} {docType.value} {period}")

    try:
        print(f"    Downloading from EDGAR...")
        fileBytes = await downloadDocumentBytes(url)

        s3Key = f"{S3_DOCUMENTS_PREFIX}/{company.value.lower()}/{docId}.pdf"
        uploadRawDocument(fileBytes, s3Key)
        print(f"    Uploaded to S3: {s3Key}")

        rawText = extractTextFromBytes(fileBytes, url)
        print(f"    Extracted {len(rawText)} characters of text")

        metadata = IngestionMetadataSchema(
            company=company,
            docType=docType,
            period=period,
            url=url,
            namespace=PINECONE_PUBLIC_NAMESPACE
        )
        chunks = chunkText(rawText, metadata)
        print(f"    Created {len(chunks)} chunks")

        chunkTexts  = [chunk.text for chunk in chunks]
        embeddings  = buildEmbeddingsBatch(chunkTexts)
        print(f"    Built {len(embeddings)} embeddings")

        upsertedCount = upsertToPinecone(chunks, embeddings, PINECONE_PUBLIC_NAMESPACE)
        print(f"    Upserted {upsertedCount} vectors to Pinecone")

        processedDoc = ProcessedDocSchema(
            docId=docId,
            company=company.value,
            docType=docType.value,
            period=period,
            s3Key=s3Key,
            namespace=PINECONE_PUBLIC_NAMESPACE,
            chunksCount=len(chunks),
            status="completed",
            processedAt=datetime.utcnow().isoformat()
        )
        insertProcessedDoc(processedDoc)
        print(f"  [DONE] {company.value} {docType.value} {period} — {len(chunks)} chunks\n")

    except Exception as e:
        print(f"  [FAIL] {company.value} {docType.value} {period} — Error: {e}\n")

async def runInitialIngestion() -> None:
    print("=" * 60)
    print("HiStock — Initial Document Ingestion")
    print("=" * 60)
    print(f"Documents to process: {len(DOCUMENTS_TO_INGEST)}\n")

    for i, docConfig in enumerate(DOCUMENTS_TO_INGEST, 1):
        print(f"[{i}/{len(DOCUMENTS_TO_INGEST)}]", end=" ")
        await ingestDocument(docConfig)

    print("=" * 60)
    print(f"Ingestion complete.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(runInitialIngestion())
