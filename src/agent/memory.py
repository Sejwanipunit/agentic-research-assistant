from langchain_core.messages import HumanMessage, AIMessage
from src.agent.state import AgentState

class ConversationMemory:
    """
    Manages multi-turn conversation history.
    Keeps track of all messages across multiple queires
    so the agent can reference previous context.
    """
    
    def __init__(self, max_history: int = 10):
        """
        max_history: maximum number of conversatuion turns to keep.
        Older messages get dropped to avoid hitting context window limits.
        """
        
        self.messages = []
        self.max_history = max_history
        
    def add_user_message(self, content: str):
        """Add a user message to history."""
        self.messages.append(HumanMessage(content=content))
        self._trim()
        
    def add_ai_message(self, content: str):
        """Add an assistant response to history."""
        self.messages.append(AIMessage(content=content))
        self._trim()
        
    def _trim(self):
        """
        Keep only the last max_history messages.
        Prevent context window overflow on long conversations.
        Each 'turn' = 1 user message + 1 AI message = 2 messages.
        So max_history=10 keeps last 5 full turns.
        """
        if len(self.messages) > self.max_history * 2:
            self.messages = self.messages[-(self.max_history * 2):]
            
    def clear(self):
        """Clear all conversation history."""
        self.messages = []
        
    def get_initial_state(self, user_input: str) -> AgentState:
        """
        Builds the initial AgentState for a new query.
        Includes full conversation history so the agent
        has context from previous turns."""
        
        #Add current user message to history
        self.add_user_message(user_input)
        
        return AgentState(
            messages=self.get_messages(),
            tool_call_count=0
        )
    