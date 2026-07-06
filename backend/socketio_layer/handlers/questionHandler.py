import uuid
from pydantic import ValidationError
from socketio_layer.socketServer import sio
from schema.socketSchema import AskQuestionEventSchema, QuestionReceivedEventSchema, AiDoneEventSchema
from enums.socketEventEnum import SocketEventEnum
from socketio_layer.middleware.rateLimitMiddleware import checkRateLimit
from agent.graph import agentGraph
from controller.agentController import isQueryInScope, OUT_OF_SCOPE_MESSAGE
from repo.messageRepo import insertMessage
from repo.sessionRepo import addTickersToSessionRecord
from utils.tickerExtractor import extractTickersFromText

def registerQuestionHandlers():

    @sio.on(SocketEventEnum.ASK_QUESTION)
    async def onAskQuestion(sid, data):
        try:
            eventData = AskQuestionEventSchema(**data)
        except ValidationError as e:
            await sio.emit(SocketEventEnum.ERROR, {"code": "INVALID_INPUT", "message": str(e)}, to=sid)
            return

        session  = await sio.get_session(sid)
        userId   = session["userId"]
        userName = session.get("name", "User")
        userPlan = session.get("plan", "free")

        allowed = await checkRateLimit(userId, userPlan)
        if not allowed:
            await sio.emit(SocketEventEnum.RATE_LIMIT_EXCEEDED, {
                "message": "Daily query limit reached. This demo allows 10 queries/day on the free plan."
            }, to=sid)
            return

        if not isQueryInScope(eventData.question):
            await sio.emit(SocketEventEnum.AI_DONE, AiDoneEventSchema(
                messageId=eventData.messageId,
                answer=OUT_OF_SCOPE_MESSAGE,
                sources=[]
            ).model_dump(), room=eventData.sessionId)
            return

        await sio.emit(
            SocketEventEnum.QUESTION_RECEIVED,
            QuestionReceivedEventSchema(
                question=eventData.question, askedBy=userName, messageId=eventData.messageId
            ).model_dump(),
            room=eventData.sessionId
        )

        initialState = {
            "question":         eventData.question,
            "sessionId":        eventData.sessionId,
            "userId":           userId,
            "company":          "both",
            "messageId":        eventData.messageId,
            "planSteps":        [],
            "toolCallHistory":  [],
            "subQueryResults":  [],
            "retrievedChunks":  [],
            "hasEnoughContext": False,
            "iterationCount":   0,
            "finalAnswer":      None,
            "sources":          []
        }

        finalState = await agentGraph.ainvoke(initialState)
        finalAnswer = finalState.get("finalAnswer", "")
        sources     = finalState.get("sources", [])

        await sio.emit(
            SocketEventEnum.AI_DONE,
            AiDoneEventSchema(messageId=eventData.messageId, answer=finalAnswer, sources=sources).model_dump(),
            room=eventData.sessionId
        )

        await insertMessage(
            sessionId=eventData.sessionId,
            userId=userId,
            question=eventData.question,
            answer=finalAnswer,
            sources=sources
        )

        mentionedTickers = extractTickersFromText(finalAnswer)
        if mentionedTickers:
            await addTickersToSessionRecord(eventData.sessionId, mentionedTickers)
