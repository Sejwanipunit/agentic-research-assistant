import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    

    # Tavily
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # LangSmith
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "agentic-research-assistant")

    # Agent limits
    MAX_TOOL_CALLS: int = 10        # max tool calls per query (prevents infinite loops)
    MODEL_NAME: str = "llama-3.3-70b-versatile" # xAI model name
    
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME: str = "gemini-2.5-flash"