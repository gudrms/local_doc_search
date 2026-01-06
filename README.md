# 사내 문서 검색기 (Local Document Searcher)

로컬 LLM과 GPU 가속을 활용하여 사내 규정(HWP, DOCX, TXT) 문서를 안전하게 검색하고 질의응답할 수 있는 도구입니다.

## 🎯 프로젝트 목적
- **보안 강화**: 외부 API를 사용하지 않고 로컬 환경에서 LLM을 구동하여 데이터 유출 방지
- **업무 효율화**: 방대한 규정 문서에서 필요한 정보를 즉시 검색
- **GPU 가속**: NVIDIA GPU를 활용하여 빠른 응답 속도 제공

## 🚀 시작하기

### 필수 요구사항
- **Python**: 3.10 이상
- **CUDA**: 12.x (GPU 사용 시)
- **Ollama**: 로컬 LLM 실행기
- **NVIDIA GPU**: 4GB VRAM 이상 권장

### 설치 방법

1. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   ```

2. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   pip install pyhwp  # HWP 파일 파싱용 (선택)
   ```

3. **CUDA 12.x 설치** (GPU 사용 시)
   - https://developer.nvidia.com/cuda-downloads
   - Ollama가 GPU를 인식하도록 CUDA 12 필수

4. **Ollama 설치 및 모델 준비**
   ```bash
   # Ollama 설치: https://ollama.com/download

   # 모델 다운로드 (EXAONE 3.5 2.4B - 한국어 최적화)
   ollama pull exaone3.5:2.4b

   # Ollama 실행 (별도 터미널)
   ollama serve
   ```

5. **GPU 인식 확인**
   ```bash
   # 다른 터미널에서
   ollama ps
   # PROCESSOR 열에 "GPU"가 표시되어야 함
   ```

### 실행 방법

```bash
streamlit run app.py
```

앱이 실행되면:
1. 사이드바에서 **"문서 데이터 갱신 (인덱싱)"** 버튼 클릭
2. `./doc` 폴더의 문서(HWP, DOCX, TXT) 자동 인덱싱
3. 질문 입력 후 답변 확인

## 📂 주요 기능
- **다양한 문서 파싱**:
  - **HWP**: HWP 5.0 (OLE2) 및 HWPX (ZIP/XML) 형식 지원
  - **DOCX**: Word 문서 지원 (표 및 텍스트 추출 최적화)
  - **TXT**: 일반 텍스트 파일 지원
- **RAG (검색 증강 생성)**:
  - 유사도 검색(Similarity Search) 기반 관련 조문 추출
  - 청크 크기 2000자, 중복 300자로 규정 맥락 보존
- **GPU 가속**: CUDA 지원으로 LLM(EXAONE 3.5) 추론 속도 대폭 향상
- **출처 표시**: 답변에 인용된 문서명 및 원문 미리보기 제공

## 🛠️ 기술 스택
- **UI**: Streamlit
- **LLM**: Ollama (exaone3.5:2.4b) with GPU
- **RAG**: LangChain, ChromaDB
- **Embedding**: HuggingFace (jhgan/ko-sroberta-multitask)
- **Document Loader**: python-docx, olefile, pyhwp (fallback)
