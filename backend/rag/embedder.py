from sentence_transformers import SentenceTransformer
from constant.appConstants import EMBEDDING_MODEL_NAME

_embeddingModel = None

def getEmbeddingModel() -> SentenceTransformer:
    global _embeddingModel
    if _embeddingModel is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
        _embeddingModel = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Embedding model loaded.")
    return _embeddingModel

def buildEmbedding(text: str) -> list[float]:
    model  = getEmbeddingModel()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()

def buildEmbeddingsBatch(texts: list[str]) -> list[list[float]]:
    model   = getEmbeddingModel()
    vectors = model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True)
    return [v.tolist() for v in vectors]
