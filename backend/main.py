# main.py
# Phase 3: Mount Socket.io as a combined ASGI app alongside FastAPI.
# The price ticker worker runs as a background asyncio task on startup.

import asyncio
import socketio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.testRouter import router as testRouter

# ── Socket.io imports ─────────────────────────────────────────────────────────
from socketio_layer.socketServer import sio
from socketio_layer.middleware.authMiddleware import registerAuthMiddleware
from socketio_layer.handlers.sessionHandler import registerSessionHandlers
from socketio_layer.handlers.questionHandler import registerQuestionHandlers
from socketio_layer.handlers.presenceHandler import registerPresenceHandlers
from worker.priceTickerWorker import startPriceTickerWorker

# ── Register all Socket.io handlers and middleware ────────────────────────────
registerAuthMiddleware()
registerSessionHandlers()
registerQuestionHandlers()
registerPresenceHandlers()

# ── Background task reference (cancelled on shutdown) ─────────────────────────
_priceTickerTask = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: launch the background price ticker worker.
    Shutdown: cancel the worker gracefully.
    """
    global _priceTickerTask
    _priceTickerTask = asyncio.create_task(startPriceTickerWorker())
    print("[main] Price ticker worker launched")
    yield
    if _priceTickerTask:
        _priceTickerTask.cancel()
        try:
            await _priceTickerTask
        except asyncio.CancelledError:
            pass
    print("[main] Price ticker worker cancelled")

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="HiStock",
    description="Real-Time Stock Research Co-pilot — NVDA & TSLA",
    version="0.3.0",
    lifespan=lifespan
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
    return {"status": "ok", "phase": "3 — Real-Time (Socket.io)", "version": "0.3.0"}

# ── Combined ASGI app: Socket.io + FastAPI ────────────────────────────────────
# Socket.io handles WebSocket connections at /socket.io/
# FastAPI handles all REST requests
# uvicorn should target: main:combinedApp
combinedApp = socketio.ASGIApp(sio, app)
