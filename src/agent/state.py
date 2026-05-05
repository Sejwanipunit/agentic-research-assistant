from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    The state that flows through every node in our LangGraph graph.

    - messages: full conversation history (user, assistant, tool results)
      operator.add means each node APPENDS to this list rather than replacing it
      This is how LangGraph accumulates context across the ReAct loop

    - tool_call_count: tracks how many tool calls we've made this turn
      Used to prevent infinite loops (safety limit)
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_call_count: int
    