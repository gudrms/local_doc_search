import streamlit as st
import os
import sys

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import RagEngine

st.set_page_config(page_title="사내 문서 검색기", layout="wide")

@st.cache_resource
def get_engine():
    return RagEngine()

try:
    engine = get_engine()
except Exception as e:
    st.error(f"엔진 초기화 실패: {e}")
    st.stop()

st.title("📑 사내 규정 검색기 (PoC)")

with st.sidebar:
    st.header("설정")

    # 문서 목록 표시
    doc_folder = os.path.join(os.path.dirname(__file__), "doc")
    if os.path.exists(doc_folder):
        doc_files = []
        for file in os.listdir(doc_folder):
            if file.lower().endswith(('.docx', '.txt', '.hwp')):
                doc_files.append(file)

        if doc_files:
            st.markdown("### 📂 참조 문서 목록")
            for file in sorted(doc_files):
                file_ext = file.split('.')[-1].upper()
                st.markdown(f"- 📄 {file} `[{file_ext}]`")
            st.caption(f"총 {len(doc_files)}개 문서")
        else:
            st.warning("⚠️ doc 폴더에 문서가 없습니다")
    else:
        st.error("❌ doc 폴더를 찾을 수 없습니다")

    st.markdown("---")

    if st.button("문서 데이터 갱신 (인덱싱)"):
        with st.spinner("문서를 읽고 인덱싱 중입니다..."):
            # Define paths to scan
            target_paths = [
                os.path.join(os.path.dirname(__file__), "doc")
            ]

            docs = engine.load_documents(target_paths)
            if docs:
                engine.create_index(docs)
                st.success(f"인덱싱 완료! ({len(docs)}개 문서)")
            else:
                st.warning("문서를 찾을 수 없거나 텍스트를 추출할 수 없습니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("규정에 대해 물어보세요 (예: 육아 휴직 규정이 궁금해?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("문서 검색 및 답변 생성 중..."):
            try:
                response = engine.ask(prompt)
                answer = response.get("result", "죄송합니다. 답변을 생성하지 못했습니다.")
                sources = response.get("source_documents", [])
                
                st.markdown(answer)

                if sources:
                    st.markdown("---")
                    st.markdown("### 📚 참고 문서 및 인용 내용")

                    for i, doc in enumerate(sources, 1):
                        source_name = doc.metadata.get("source", "Unknown")
                        content = doc.page_content

                        # 인용 내용 표시 (최대 300자)
                        preview = content[:300] + "..." if len(content) > 300 else content

                        with st.expander(f"📄 {i}. {source_name}"):
                            st.text(preview)
                            st.caption(f"전체 길이: {len(content)} 글자")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"오류 발생: {e}")
