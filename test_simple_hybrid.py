"""
간단한 하이브리드 검색
BM25 + 벡터 검색 수동 결합
"""
import sys, os, io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from rag_engine import RagEngine

print("=" * 60)
print("하이브리드 검색 테스트 (간단 버전)")
print("=" * 60)

# 1. 기존 엔진 로드
engine = RagEngine()
engine.load_index()

# 2. 테스트 질문
test_queries = [
    "제5장에 대해 알려줘",
    "규정 2장에 대해 알려줘",
    "15조에 대해 알려줘"
]

for query in test_queries:
    print("\n" + "=" * 60)
    print(f"질의: {query}")
    print("=" * 60)
    
    # 벡터 검색
    retriever = engine.vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    
    print(f"\n검색된 문서 ({len(docs)}개):")
    for i, doc in enumerate(docs, 1):
        content = doc.page_content[:200].replace('\n', ' ')
        print(f"  [{i}] {doc.metadata.get('source', 'Unknown')}")
        print(f"      {content}...")
        
        # 제목 매칭 확인
        has_match = query.replace("제", "").replace("장", "").replace("조", "").replace(" ", "").replace("에", "").replace("대해", "").replace("알려줘", "").replace("규정", "")
        if has_match in doc.page_content:
            print(f"      [OK] 키워드 '{has_match}' 발견!")
    
    # LLM 답변
    print("\n[LLM 답변]")
    response = engine.ask(query)
    print(response.get('result', ''))
