from langgraph.graph import StateGraph, END
from langraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from src.agent.state import AgentState
from src.config import Config

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a research assistant with access to tools.

For every query:
1. THINK about what information you need
2. CALL a tool if needed
3. OBSERVE the result
4. REPEAT until you have enough to answer
5. Give a clear, well-structured final answer

Be concise in your reasoning. Cite sources when using web search."""


# ── LLM setup ──────────────────────────────────────────────────────────────────
def get_llm(tools: list):
    """
    Returns the LLM bound to our tools.
    .bind_tools() tells the model what tools exist and their schemas —
    so it can decide to call them by emitting a tool_call in its response.
    """
    llm = ChatOpenAI(
        model=Config.MODEL_NAME,
        api_key=Config.XAI_API_KEY,
        base_url=Config.XAI_BASE_URL,
        temperature=0,          # deterministic — important for agents
        streaming=True,
    )
    return llm.bind_tools(tools)


# ── Nodes ──────────────────────────────────────────────────────────────────────
def reason_node(state: AgentState, llm):
    """
    The THINK step of ReAct.
    Takes the current state (all messages so far) and asks the LLM:
    'What should I do next — call a tool or give a final answer?'
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    response = llm.invoke(messages)
    return {
        "messages": [response],
        "tool_call_count": state["tool_call_count"]
    }


def should_continue(state: AgentState) -> str:
    """
    The ROUTING logic — this is the edge decision in LangGraph.

    Checks the last message:
    - If it has tool_calls → go to 'tools' node (ACT step)
    - If no tool_calls → go to END (agent is done)
    - If we've hit MAX_TOOL_CALLS → force END (safety valve)
    """
    last_message = state["messages"][-1]

    if state["tool_call_count"] >= Config.MAX_TOOL_CALLS:
        return END

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# ── Graph builder ──────────────────────────────────────────────────────────────
def build_graph(tools: list):
    """
    Wires up the ReAct loop as a LangGraph StateGraph.

    Flow:
        [START] → reason → should_continue → tools → reason → ... → [END]

    The loop continues until the LLM stops calling tools.
    """
    llm = get_llm(tools)

    # ToolNode is LangGraph's built-in node that executes tool calls
    # It reads tool_calls from the last message, runs them, returns results
    tool_node = ToolNode(tools)

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("reason", lambda state: reason_node(state, llm))
    graph.add_node("tools", tool_node)

    # Set entry point
    graph.set_entry_point("reason")

    # Add conditional edge: after reasoning, either call tools or end
    graph.add_conditional_edges("reason", should_continue)

    # After tools run, always go back to reason (the loop!)
    graph.add_edge("tools", "reason")

    return graph.compile()