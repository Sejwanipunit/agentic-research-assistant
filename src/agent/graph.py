from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

from src.agent.state import AgentState
from src.config import Config

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful research assistant with access to these tools:

1. web_search(query) - Search the internet for current information
2. code_executor(code) - Execute Python code and return output
3. doc_lookup(query) - Search local documents

IMPORTANT RULES:
- Always use web_search for questions about current events or facts
- Always use code_executor when asked to run, write, or calculate with code
- Use doc_lookup for questions about local documents
- After getting tool results, provide a clear final answer
- If no tool is needed, answer directly"""


# ── LLM setup ──────────────────────────────────────────────────────────────────
def get_llm(tools: list):
    """
    Returns the LLM bound to our tools.
    .bind_tools() tells the model what tools exist and their schemas —
    so it can decide to call them by emitting a tool_call in its response.
    """
    llm = ChatGoogleGenerativeAI(
        model=Config.MODEL_NAME,
        google_api_key=Config.GOOGLE_API_KEY,
        temperature=0,
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
    
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"🔧 Tool called: {tool_call['name']}")
            print(f"   Args: {tool_call['args']}")
            
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