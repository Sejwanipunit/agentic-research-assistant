# 50 benchmark queries across 3 categories
# Each has an expected_keywords list — if response contains
# enough of these, we consider the query successfully answered

BENCHMARK_QUERIES = [
    # ── Web Search queries (need live information) ──────────────────
    {
        "id": 1,
        "category": "web_search",
        "query": "What is LangGraph and how does it differ from LangChain?",
        "expected_keywords": ["langgraph", "langchain", "graph", "state", "nodes"]
    },
    {
        "id": 2,
        "category": "web_search",
        "query": "What are the latest developments in RAG pipelines?",
        "expected_keywords": ["retrieval", "augmented", "generation", "chunk", "embed"]
    },
    {
        "id": 3,
        "category": "web_search",
        "query": "Explain the ReAct pattern in LLM agents",
        "expected_keywords": ["reason", "act", "observe", "tool", "loop"]
    },
    {
        "id": 4,
        "category": "web_search",
        "query": "What is Tavily and why is it used for AI agents?",
        "expected_keywords": ["tavily", "search", "agent", "api", "llm"]
    },
    {
        "id": 5,
        "category": "web_search",
        "query": "What is GGUF format in LLM quantization?",
        "expected_keywords": ["gguf", "quantiz", "llama", "model", "format"]
    },
    {
        "id": 6,
        "category": "web_search",
        "query": "How does vector similarity search work?",
        "expected_keywords": ["vector", "embed", "similarity", "cosine", "distance"]
    },
    {
        "id": 7,
        "category": "web_search",
        "query": "What is the difference between BM25 and dense retrieval?",
        "expected_keywords": ["bm25", "dense", "sparse", "retrieval", "hybrid"]
    },
    {
        "id": 8,
        "category": "web_search",
        "query": "What is QLoRA and how does it reduce GPU memory?",
        "expected_keywords": ["qlora", "lora", "quantiz", "memory", "fine-tun"]
    },
    {
        "id": 9,
        "category": "web_search",
        "query": "What is RAGAS and what metrics does it measure?",
        "expected_keywords": ["ragas", "faithfulness", "relevancy", "recall", "metric"]
    },
    {
        "id": 10,
        "category": "web_search",
        "query": "How does LangSmith help with LLM observability?",
        "expected_keywords": ["langsmith", "trac", "observ", "latency", "token"]
    },
    {
        "id": 11,
        "category": "web_search",
        "query": "What is the difference between GPT-4 and GPT-4o?",
        "expected_keywords": ["gpt", "multimodal", "faster", "openai", "model"]
    },
    {
        "id": 12,
        "category": "web_search",
        "query": "What is Qdrant and what makes it suitable for production?",
        "expected_keywords": ["qdrant", "vector", "production", "filter", "index"]
    },
    {
        "id": 13,
        "category": "web_search",
        "query": "What is prompt engineering and why does it matter?",
        "expected_keywords": ["prompt", "engineer", "instruct", "llm", "output"]
    },
    {
        "id": 14,
        "category": "web_search",
        "query": "What is Mistral 7B and why is it popular for fine-tuning?",
        "expected_keywords": ["mistral", "7b", "fine-tun", "open", "model"]
    },
    {
        "id": 15,
        "category": "web_search",
        "query": "Explain how attention mechanism works in transformers",
        "expected_keywords": ["attention", "transform", "query", "key", "value"]
    },
    {
        "id": 16,
        "category": "web_search",
        "query": "What is FastAPI and why use it for ML model serving?",
        "expected_keywords": ["fastapi", "async", "api", "serve", "python"]
    },
    {
        "id": 17,
        "category": "web_search",
        "query": "What is the difference between RAG and fine-tuning?",
        "expected_keywords": ["rag", "fine-tun", "retrieval", "train", "knowledge"]
    },
    {
        "id": 18,
        "category": "web_search",
        "query": "What is FAISS and how does it index vectors?",
        "expected_keywords": ["faiss", "index", "vector", "facebook", "search"]
    },
    {
        "id": 19,
        "category": "web_search",
        "query": "What are AI agents and how do they differ from chatbots?",
        "expected_keywords": ["agent", "tool", "autonom", "chatbot", "action"]
    },
    {
        "id": 20,
        "category": "web_search",
        "query": "What is Llama.cpp and what problem does it solve?",
        "expected_keywords": ["llama.cpp", "cpu", "inference", "quantiz", "embed"]
    },

    # ── Code Execution queries (need Python execution) ───────────────
    {
        "id": 21,
        "category": "code_execution",
        "query": "Write and run Python code to calculate the first 10 Fibonacci numbers",
        "expected_keywords": ["0", "1", "1", "2", "3", "5", "8", "13", "21", "34"]
    },
    {
        "id": 22,
        "category": "code_execution",
        "query": "Write Python code to sort this list and show the result: [5, 2, 8, 1, 9, 3]",
        "expected_keywords": ["1", "2", "3", "5", "8", "9"]
    },
    {
        "id": 23,
        "category": "code_execution",
        "query": "Calculate the mean and standard deviation of [10, 20, 30, 40, 50] using Python",
        "expected_keywords": ["30", "mean", "standard", "deviation", "14"]
    },
    {
        "id": 24,
        "category": "code_execution",
        "query": "Write Python to check if a string is a palindrome for the word 'racecar'",
        "expected_keywords": ["racecar", "palindrome", "true", "yes"]
    },
    {
        "id": 25,
        "category": "code_execution",
        "query": "Run Python code to count word frequency in 'the quick brown fox jumps over the lazy dog'",
        "expected_keywords": ["the", "2", "quick", "brown", "fox"]
    },
    {
        "id": 26,
        "category": "code_execution",
        "query": "Write Python to find all prime numbers between 1 and 50",
        "expected_keywords": ["2", "3", "5", "7", "11", "13", "17", "19", "23"]
    },
    {
        "id": 27,
        "category": "code_execution",
        "query": "Calculate compound interest for principal=1000, rate=5%, time=3 years using Python",
        "expected_keywords": ["1157", "compound", "interest"]
    },
    {
        "id": 28,
        "category": "code_execution",
        "query": "Write Python code to reverse a string and show result for 'LangGraph'",
        "expected_keywords": ["hparGgnaL", "reverse"]
    },
    {
        "id": 29,
        "category": "code_execution",
        "query": "Use Python to demonstrate list comprehension by squaring numbers 1 to 10",
        "expected_keywords": ["1", "4", "9", "16", "25", "36", "49", "64", "81", "100"]
    },
    {
        "id": 30,
        "category": "code_execution",
        "query": "Write Python to convert Celsius to Fahrenheit for 0, 100, and 37 degrees",
        "expected_keywords": ["32", "212", "98.6"]
    },
    {
        "id": 31,
        "category": "code_execution",
        "query": "Show a Python dictionary example mapping 3 programming languages to their use cases",
        "expected_keywords": ["python", "dict", "{"]
    },
    {
        "id": 32,
        "category": "code_execution",
        "query": "Write Python to find the largest and smallest number in [45, 12, 78, 3, 56, 89, 23]",
        "expected_keywords": ["89", "3", "largest", "smallest"]
    },
    {
        "id": 33,
        "category": "code_execution",
        "query": "Write Python to demonstrate a simple class with __init__ and a method",
        "expected_keywords": ["class", "__init__", "self", "def"]
    },
    {
        "id": 34,
        "category": "code_execution",
        "query": "Use Python to calculate factorial of 10",
        "expected_keywords": ["3628800", "factorial"]
    },
    {
        "id": 35,
        "category": "code_execution",
        "query": "Write Python code to flatten a nested list [[1,2],[3,4],[5,6]]",
        "expected_keywords": ["1", "2", "3", "4", "5", "6", "flatten"]
    },

    # ── Reasoning queries (multi-hop, combine knowledge) ─────────────
    {
        "id": 36,
        "category": "reasoning",
        "query": "Compare RAG and fine-tuning — when would you use each?",
        "expected_keywords": ["rag", "fine-tun", "retrieval", "train", "use case"]
    },
    {
        "id": 37,
        "category": "reasoning",
        "query": "What are the tradeoffs between FAISS and Qdrant for production?",
        "expected_keywords": ["faiss", "qdrant", "scale", "persist", "production"]
    },
    {
        "id": 38,
        "category": "reasoning",
        "query": "Explain how you would build a production RAG system from scratch",
        "expected_keywords": ["chunk", "embed", "retriev", "llm", "evaluat"]
    },
    {
        "id": 39,
        "category": "reasoning",
        "query": "What makes an LLM agent different from a simple LLM chain?",
        "expected_keywords": ["agent", "tool", "loop", "decision", "chain"]
    },
    {
        "id": 40,
        "category": "reasoning",
        "query": "How would you evaluate the quality of a RAG system?",
        "expected_keywords": ["ragas", "faithfulness", "relevancy", "recall", "metric"]
    },
    {
        "id": 41,
        "category": "reasoning",
        "query": "What are the main challenges in deploying LLMs in production?",
        "expected_keywords": ["latency", "cost", "hallucin", "scale", "monitor"]
    },
    {
        "id": 42,
        "category": "reasoning",
        "query": "Explain the difference between zero-shot and few-shot prompting",
        "expected_keywords": ["zero-shot", "few-shot", "example", "prompt", "context"]
    },
    {
        "id": 43,
        "category": "reasoning",
        "query": "What is chunking strategy in RAG and why does it matter?",
        "expected_keywords": ["chunk", "size", "overlap", "retriev", "context"]
    },
    {
        "id": 44,
        "category": "reasoning",
        "query": "How does hybrid search improve over pure semantic search?",
        "expected_keywords": ["hybrid", "bm25", "dense", "keyword", "semantic"]
    },
    {
        "id": 45,
        "category": "reasoning",
        "query": "What is context window and why does it matter for LLM applications?",
        "expected_keywords": ["context", "window", "token", "limit", "memory"]
    },
    {
        "id": 46,
        "category": "reasoning",
        "query": "Explain temperature in LLMs and when to set it to 0",
        "expected_keywords": ["temperature", "deterministic", "random", "creative", "agent"]
    },
    {
        "id": 47,
        "category": "reasoning",
        "query": "What is the role of embeddings in a RAG pipeline?",
        "expected_keywords": ["embed", "vector", "semantic", "similar", "retriev"]
    },
    {
        "id": 48,
        "category": "reasoning",
        "query": "How does cross-encoder reranking improve RAG retrieval?",
        "expected_keywords": ["rerank", "cross-encoder", "retriev", "relevance", "score"]
    },
    {
        "id": 49,
        "category": "reasoning",
        "query": "What are hallucinations in LLMs and how can RAG reduce them?",
        "expected_keywords": ["hallucin", "fact", "retriev", "ground", "rag"]
    },
    {
        "id": 50,
        "category": "reasoning",
        "query": "Explain how LangSmith helps debug and monitor LLM applications",
        "expected_keywords": ["langsmith", "trace", "debug", "latency", "monitor"]
    }
]