from pinecone import Pinecone
from constant.appConstants import PINECONE_API_KEY, PINECONE_INDEX_NAME

_pineconeIndex = None

def getPineconeIndex():
    global _pineconeIndex
    if _pineconeIndex is None:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        _pineconeIndex = pc.Index(PINECONE_INDEX_NAME)
    return _pineconeIndex
