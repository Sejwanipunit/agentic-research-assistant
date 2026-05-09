from src.tools.web_search import web_search
from src.tools.code_executor import code_executor
from src.tools.doc_lookup import doc_lookup

# This list gets passed to build_graph()
ALL_TOOLS = [web_search, code_executor, doc_lookup]