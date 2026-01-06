import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from rag_engine import RagEngine

print("=" * 60)
print("'2장' 검색 문제 디버깅")
print("=" * 60)

engine = RagEngine()
engine.load_index()

# 사용자의 실제 질문
query = "규정 2장에 대해 알려줘"

print(f"\n질의: '{query}'")
print("=" * 60)

# 벡터 검색 결과 자세히 보기
retriever = engine.vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

docs = retriever.invoke(query)

print(f"\n검색된 문서 수: {len(docs)}개\n")

for i, doc in enumerate(docs, 1):
    print(f"{'='*60}")
    print(f"[문서 {i}] {doc.metadata.get('source', 'Unknown')}")
    print(f"{'='*60}")
    print(f"내용 (처음 500자):")
    print(doc.page_content[:500])
    print(f"\n... (총 {len(doc.page_content)} 글자)")
    print()

# 실제 LLM 답변
print("\n" + "="*60)
print("LLM 최종 답변")
print("="*60)
response = engine.ask(query)
print(response.get('result', ''))
