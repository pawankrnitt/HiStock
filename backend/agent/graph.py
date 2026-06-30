from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.plannerNode import plannerNode
from agent.nodes.toolExecutorNode import toolExecutorNode
from agent.nodes.reflectNode import reflectNode, shouldContinue
from agent.nodes.responderNode import responderNode

def buildAgentGraph():
    """
    Build and compile the ReAct agent graph.

    Graph flow:
      planner → toolExecutor → reflect → (continue → toolExecutor) | (end → responder) → END

    Conditional edge at reflect:
      shouldContinue() returns "continue" → loop back to toolExecutor
      shouldContinue() returns "end"      → proceed to responder
    """
    graph = StateGraph(AgentState)

    graph.add_node("planner",      plannerNode)
    graph.add_node("toolExecutor", toolExecutorNode)
    graph.add_node("reflect",      reflectNode)
    graph.add_node("responder",    responderNode)

    graph.set_entry_point("planner")

    graph.add_edge("planner",      "toolExecutor")
    graph.add_edge("toolExecutor", "reflect")

    graph.add_conditional_edges(
        "reflect",
        shouldContinue,
        {
            "continue": "toolExecutor",    # loop: get more context
            "end":      "responder"        # enough context: generate answer
        }
    )

    graph.add_edge("responder", END)

    return graph.compile()

# Compile once at module import — reuse across all requests
agentGraph = buildAgentGraph()
