import sys
print(sys.executable)
try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    from langchain.chains import RetrievalQA
    print("Import successful: from langchain.chains import RetrievalQA")
except ImportError as e:
    print(f"Import failed: {e}")
    try:
        from langchain.chains.retrieval_qa.base import RetrievalQA
        print("Import successful: from langchain.chains.retrieval_qa.base import RetrievalQA")
    except ImportError as e2:
        print(f"Explicit import failed: {e2}")

try:
    import langchain_community
    print(f"LangChain Community version: {langchain_community.__version__}")
except ImportError:
    print("LangChain Community not found")
