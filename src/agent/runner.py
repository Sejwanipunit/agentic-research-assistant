from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import AIMessage

from src.agent.memory import ConversationMemory
from src.agent.graph import build_graph
from src.tools import ALL_TOOLS, build_vectorstore


class AgentRunner:
    """
    The main interface for running the agent.
    handles graph execution, memory managment, and streaming.
    """
    
    def __init__(self):
        #Build the LangGraph graph with all tools
        self.graph: CompiledStateGraph = build_graph(ALL_TOOLS)
        
        #initialize conversation memory
        self.memory = ConversationMemory(max_history=10)
        
        #Build document vectorstore at startup
        build_vectorstore()
        print("Agent ready.")
        
    def run(self, user_input: str) -> str:
        """
        Run a single query through the agent.
        Return the final response as a string
        """
        # Get initial state with conversation history
        state = self.memory.get_initial_state(user_input)
        
        #invoke the graph
        final_state = self.graph.invoke(state)
        
        #Extract the last AI message as the response
        response = self._extract_response(final_state)
        
        #save to memory for next turn
        self.memory.add_ai_message(response)
        
        return response
    
    def stream(self, user_input: str):
        """
        Stream the agent's response token by token.
        Yields text chunks as they are generated.

        Usage:
            for chunk in agent.stream("What is X?"):
                print(chunk, end="", flush=True)
        """
        state = self.memory.get_initial_state(user_input)
        
        # .stream() yields state updates at each node
        for chunk in self.graph.stream(state, stream_mode="updates"):
            #Only yield from the reason node (not tool results)
            if "reason" in chunk:
                messages = chunk["reason"].get("messages", [])
                for msg in messages:
                    if isinstance(msg, AIMessage) and msg.content:
                        yield msg.content
                        
        #Save full response to memory
        final_state = self.graph.invoke(
            self.memory.get_initial_state(user_input)
        )
        self.memory.add.ai_message(
            self._extract_response(final_state)
        )
        
        def _extract_response(self, final_state: dict) -> str:
            """
        Pulls the last AIMessage content from final state.
        Skips tool messages and intermediate reasoning.
        """
        messages = final_state.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        return "No response generated."

    def clear_memory(self):
        """Reset conversation history."""
        self.memory.clear()
        print("Memory cleared.")
            
        
    