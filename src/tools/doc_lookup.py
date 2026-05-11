import os
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config
from src.tools.schemas import DocLookupInput 


_vectorstore = None

def _get_embeddings():
    
    """
    Uses a local HuggingFace model for embeddings.
    Runs on CPU — no API key needed.
    Model downloads once (~90MB) and is cached locally.
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",   # small, fast, good quality
        model_kwargs={"device": "cpu"}
    )
    
def build_vectorstore(docs_path: str = "data/docs"):
    """
    Loads documents from the specified path and builds a FAISS vector index.
    Called once at startup - not on every tool call.
    """
    
    global  _vectorstore
    
    #If docs Folder is not there create one
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        with open(f"{docs_path}/sample.txt", "w") as f:
            f.write(
                "This is a sample document for the agentic research assistant. "
                "Add your own documents to the data/docs folder."
            )
            
    #Load all .txt files from the folder
    loader = DirectoryLoader(
        docs_path,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    
    #Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    
    #Build FAISS index from chunks
    _vectorstore = FAISS.from_documents(
        chunks,
        embedding=_get_embeddings()
    )
    return _vectorstore

@tool
def doc_lookup(query: str) -> str:
    """
    Search through local documents for relevant information.
    Use this when the query is about specific documents, files,
    or knowledge base content rather than general web information.
    
    Args:
        query: The search query to find relevant documents sections
        
    Returns:
        Relevant document excerpts that match the query
        
    """
    global _vectorstore
    
    try:
        #Build vectorstore if it doesn't exist
        if _vectorstore is None:
            build_vectorstore()
            
        #Similarity search
        results = _vectorstore.similarity_search(query, k=3)
        
        if not results:
            return "No relevant documents found."
        
        #Format results for the LLM
        output = []
        for i, doc in enumerate(results,1):
            source = doc.metadata.get("source", "Unknown")
            output.append(
                f"[{i}] Source: {source}\n"
                f"Content: {doc.page_content}\n"
            )
        return "\n".join(output)
    
    except Exception as e:
        return f"Document lookup failed: {str(e)}"