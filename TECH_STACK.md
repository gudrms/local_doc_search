# 기술 스택 (Tech Stack)

## Phase 1: PoC (Proof of Concept)

빠른 검증과 프로토타이핑을 위해 Python 생태계를 활용합니다.

### 1. Core Framework
- **Language**: Python 3.10+
- **UI Framework**: Streamlit
    - 선정 이유: 빠른 UI 개발, 데이터 시각화 및 채팅 인터페이스 내장.

### 2. AI & Data Pipeline
- **Orchestration**: LangChain
    - RAG 파이프라인 구축 및 LLM 연동 표준화.
- Local LLM: Ollama
    - Model: `exaone3.5:2.4b` (LG AI Research)
    - 선정 이유: 한국어 특화 성능, 경량 모델(2.4B)로 일반적인 GPU 환경에서 원활한 구동 가능.
- Vector Database: ChromaDB
    - 선정 이유: 별도 서버 없이 로컬 파일로 구동 가능, LangChain과의 높은 호환성.
- Embedding: `jhgan/ko-sroberta-multitask` (HuggingFace)
    - 선정 이유: 한국어 문장 유사도 측정에 특화된 경량 모델.

### 3. Document Processing
- **HWP Loader**: `olefile`, `pyhwp`, HWPX(XML/ZIP) 지원 커스텀 로직
- **DOCX Loader**: `python-docx` 기반 텍스트 및 표 추출
- **TXT Loader**: 기본 내장 로더

---

## Phase 2: 정식 개발 (Planned)

확장성과 안정적인 서비스를 위해 웹 애플리케이션 아키텍처로 전환합니다.

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **UI Lib**: Shadcn UI

### Backend
- **Framework**: FastAPI (Python)
    - LLM/RAG 로직과의 통합 용이성 고려.
- **Database**: PostgreSQL (pgvector)
    - 메타데이터 및 벡터 데이터 통합 관리.
