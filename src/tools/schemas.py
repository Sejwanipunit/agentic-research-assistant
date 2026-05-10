from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    """
    Input schema for the web search tool.
    """
    query: str = Field(
        description="The search query. Be specific and concise for better results.",
        min_length=3,
        max_length=200
    )
    
class CodeExecutorInput(BaseModel):
    """Input schema for the code execution tool."""
    code: str = Field(
        description="Valid Python code to execute. Must be complete and runnable.",
        min_length=1
    )
    
class DocLookupInput(BaseModel):
    """Input schema for the document lookup tool."""
    query: str = Field(
        description="Search query to find relevant sections in local documents.",
        min_length=3,
        max_length=200
    )
    
