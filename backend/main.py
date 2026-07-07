import asyncio
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.testRouter import router as testRouter
from router.authRouter import router as authRouter
from router.sessionRouter import router as sessionRouter
from router.alertRouter import router as alertRouter
from router.documentRouter import router as documentRouter
from router.reportRouter import router as reportRouter

from socketio_layer.socketServer import sio
from socketio_layer.middleware.authMiddleware import registerAuthMiddleware
from socketio_layer.handlers.sessionHandler import registerSessionHandlers
from socketio_layer.handlers.questionHandler import registerQuestionHandlers
from socketio_layer.handlers.presenceHandler import registerPresenceHandlers
from constant.appConstants import ALLOWED_ORIGINS

from worker.priceTickerWorker import startPriceTickerWorker
from middleware.errorMiddleware import globalExceptionHandler

fastApiApp = FastAPI(
    title="StockSense AI",
    description="Real-Time Stock Research Co-pilot — NVDA & TSLA",
    version="0.4.0"
)


fastApiApp.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,      # Only CloudFront domain in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


fastApiApp.add_exception_handler(Exception, globalExceptionHandler)

fastApiApp.include_router(testRouter)
fastApiApp.include_router(authRouter,     prefix="/api/v1")
fastApiApp.include_router(sessionRouter,  prefix="/api/v1")
fastApiApp.include_router(alertRouter,    prefix="/api/v1")
fastApiApp.include_router(documentRouter, prefix="/api/v1")
fastApiApp.include_router(reportRouter,   prefix="/api/v1")

@fastApiApp.get("/health")
async def healthCheck():
    return {"status": "ok", "phase": "4 — REST API", "version": "0.4.0"}

registerAuthMiddleware()
registerSessionHandlers()
registerQuestionHandlers()
registerPresenceHandlers()

@fastApiApp.on_event("startup")
async def onStartup():
    asyncio.create_task(startPriceTickerWorker())
    print("[startup] Price ticker worker started.")

app = socketio.ASGIApp(sio, other_asgi_app=fastApiApp, socketio_path="socket.io")
