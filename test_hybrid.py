import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from hybrid_rag_engine import HybridRagEngine

print("=" * 60)
print("하이브리드 검색 테스트")
print("=" * 60)

# 1. 엔진 초기화
engine = HybridRagEngine()

# 2. 문서 로드
doc_paths = ["./doc"]
print("\n[1] 문서 로딩...")
docs = engine.load_documents(doc_paths)
print(f"로드된 문서 수: {len(docs)}개")

# 3. 하이브리드 인덱스 생성
print("\n[2] 하이브리드 인덱스 생성 (BM25 + Vector)...")
engine.create_index(docs)

# 4. 테스트 질문
test_queries = [
    "규정 2장에 대해 알려줘",
    "제5장에 대해 알려줘",
    "15조에 대해 알려줘",
    "육아휴직은 어떻게 신청해?"
]

for query in test_queries:
    print("\n" + "=" * 60)
    print(f"질의: {query}")
    print("=" * 60)
    
    response = engine.ask(query)
    answer = response.get('result', '')
    sources = response.get('source_documents', [])
    
    print(f"\n답변:\n{answer}")
    print(f"\n출처 문서: {len(sources)}개")
    for i, doc in enumerate(sources[:3], 1):
        print(f"  [{i}] {doc.metadata.get('source', 'Unknown')}")
        print(f"      {doc.page_content[:100]}...")
