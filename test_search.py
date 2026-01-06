import sys
import os

# 작업 디렉토리를 스크립트 위치로 변경
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print(f"작업 디렉토리: {os.getcwd()}")

from rag_engine import RagEngine

print("=" * 60)
print("검색 디버깅 테스트")
print("=" * 60)

# 1. RAG 엔진 초기화
print("\n[1] RAG 엔진 초기화...")
engine = RagEngine()

# 2. ChromaDB 로드 시도
print("\n[2] ChromaDB 로드 시도...")
chroma_path = "./chroma_db"
print(f"   상대 경로: {chroma_path}")
print(f"   절대 경로: {os.path.abspath(chroma_path)}")
print(f"   존재 여부: {os.path.exists(chroma_path)}")

if os.path.exists(chroma_path):
    db_files = os.listdir(chroma_path)
    print(f"   파일 목록: {db_files}")
    
    # SQLite 파일 크기 확인
    sqlite_path = os.path.join(chroma_path, "chroma.sqlite3")
    if os.path.exists(sqlite_path):
        size = os.path.getsize(sqlite_path)
        print(f"   chroma.sqlite3 크기: {size:,} bytes")

result = engine.load_index()
print(f"   로드 결과: {result}")
print(f"   VectorStore 객체: {engine.vectorstore is not None}")

# 3. 문서 수 확인
if engine.vectorstore:
    try:
        count = engine.vectorstore._collection.count()
        print(f"\n[3] 인덱싱된 문서 청크 수: {count}개")
        
        if count == 0:
            print("\n   [경고] 인덱싱된 문서가 없습니다!")
            print("   Streamlit 앱에서 '문서 데이터 갱신' 버튼을 눌러주세요.")
    except Exception as e:
        print(f"\n[3] 문서 수 확인 실패: {e}")
        
    # 4. 샘플 검색 테스트
    if count > 0:
        print("\n[4] 샘플 검색 테스트...")
        test_queries = [
            "15조",
            "휴가",
            "육아휴직"
        ]
        
        for query in test_queries:
            print(f"\n{'='*50}")
            print(f"질의: '{query}'")
            print('='*50)
            try:
                response = engine.ask(query)
                answer = response.get('result', '')
                sources = response.get('source_documents', [])
                
                print(f"답변:\n{answer}\n")
                print(f"출처 문서 수: {len(sources)}개")
                
                if sources:
                    for i, doc in enumerate(sources, 1):
                        print(f"\n[출처 {i}] {doc.metadata.get('source', 'Unknown')}")
                        print(f"내용: {doc.page_content[:200]}...")
            except Exception as e:
                print(f"검색 실패: {e}")
                import traceback
                traceback.print_exc()
else:
    print("\n[ERROR] VectorStore가 로드되지 않았습니다!")
