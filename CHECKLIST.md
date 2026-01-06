# 개발 체크리스트 (Checklist)

## ✅ Phase 1: PoC (현재 단계)

### 환경 설정
- [x] 프로젝트 디렉토리 생성 및 venv 설정
- [x] 필수 패키지 설치 (`streamlit`, `langchain`, `chromadb` 등)
- [x] Ollama 설치 및 모델 준비

### 핵심 기능 구현
- [x] **HWP 로더**: `olefile` 기반 텍스트 추출 로직 구현 (`hwp_loader.py`)
- [x] **Markdown 로더**: `.md` 파일 읽기 지원
- [x] **RAG 엔진**:
    - [x] 문서 로딩 및 청킹 (Chunking)
    - [x] 임베딩 및 ChromaDB 저장
    - [x] 검색(Retrieval) 및 답변 생성 체인 구현 (`rag_engine.py`)
- [x] **UI 구현**:
    - [x] Streamlit 채팅 인터페이스 (`app.py`)
    - [x] 사이드바 설정 및 인덱싱 버튼

### 테스트 및 검증
- [ ] 실제 HWP 문서 인덱싱 테스트
- [ ] 질의응답 정확도 확인

---

## 📅 Phase 2: 정식 개발 (예정)

### 프로젝트 셋업
- [ ] Next.js 프로젝트 생성
- [ ] FastAPI 백엔드 서버 구성

### 기능 고도화
- [ ] 사용자 인증/권한 관리
- [ ] 문서 업로드 및 관리자 페이지
- [ ] 답변 만족도 평가 및 피드백 루프
