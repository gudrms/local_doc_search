import sys
import os

try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    print(f"LangChain path: {langchain.__file__}")
    
    try:
        import langchain.chains
        print("Successfully imported langchain.chains")
        print(f"langchain.chains path: {langchain.chains.__file__}")
        print(f"dir(langchain.chains): {dir(langchain.chains)}")
    except ImportError as e:
        print(f"Failed to import langchain.chains: {e}")

    try:
        from langchain.chains import RetrievalQA
        print("Successfully imported RetrievalQA from langchain.chains")
    except ImportError as e:
        print(f"Failed to import RetrievalQA from langchain.chains: {e}")
        
    try:
        from langchain.chains.retrieval_qa.base import RetrievalQA
        print("Successfully imported RetrievalQA from langchain.chains.retrieval_qa.base")
    except ImportError as e:
        print(f"Failed to import RetrievalQA from langchain.chains.retrieval_qa.base: {e}")

except ImportError as e:
    print(f"Failed to import langchain: {e}")
