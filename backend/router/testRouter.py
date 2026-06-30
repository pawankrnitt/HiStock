from fastapi import APIRouter
from controller.ragController import testRagQuery
from controller.agentController import runAgentQuery
from schema.ragSchema import RagQuerySchema, RagResponseSchema
from schema.agentSchema import AgentQuerySchema, AgentResponseSchema

router = APIRouter(prefix="/api/v1/test", tags=["test"])

@router.post("/rag", response_model=RagResponseSchema)
async def ragQueryRoute(body: RagQuerySchema) -> RagResponseSchema:
    """
    Phase 1 endpoint — simple RAG: retrieve → LLM → answer.
    Keep this for comparison with the agent endpoint.
    """
    return await testRagQuery(body)

@router.post("/agent", response_model=AgentResponseSchema)
async def agentQueryRoute(body: AgentQuerySchema) -> AgentResponseSchema:
    """
    Phase 2 endpoint — full agentic loop: plan → tools → reflect → answer.
    Input:  { question: str, company: "NVDA" | "TSLA" | null, sessionId: null }
    Output: { answer, sources, toolCallHistory, iterationCount, model, question }
    """
    return await runAgentQuery(body)
