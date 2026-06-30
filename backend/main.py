from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.testRouter import router as testRouter

app = FastAPI(
    title="HiStock",
    description="Real-Time Stock Research Co-pilot — NVDA & TSLA",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(testRouter)

@app.get("/health")
async def healthCheck():
    return {"status": "ok", "phase": "1 — Foundation & RAG", "version": "0.1.0"}
