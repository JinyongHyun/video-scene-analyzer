# Video Scene Analyzer

YouTube 영상을 다운로드하고, 원하는 정지 화면을 **SmolVLM-500M** 모델로 브라우저에서 직접 분석하는 웹 앱입니다.
모든 AI 추론은 **WebGPU**를 이용해 브라우저 내 로컬에서 실행됩니다 (외부 서버 전송 없음).

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| AI 모델 | `HuggingFaceTB/SmolVLM-500M-Instruct` (HuggingFace) |
| 추론 환경 | Transformers.js v3.6.0 + WebGPU (q4 양자화) |
| 백엔드 | Python Flask + yt-dlp |
| 프레임 캡처 | Canvas API → RawImage (448×448) |

---

## 실행 방법 (처음부터 끝까지)

### 1. 사전 준비 확인

아래 항목이 설치되어 있어야 합니다.

- **Python 3.8 이상**
  확인: `python --version`
- **Git**
  확인: `git --version`
- **브라우저**: Chrome 113+ 또는 Edge (WebGPU 지원 필요)
  ※ Firefox는 WebGPU 미지원이므로 Chrome/Edge 사용 필수

---

### 2. 저장소 클론

```bash
git clone https://github.com/JinyongHyun/video-scene-analyzer.git
cd video-scene-analyzer
```

---

### 3. Python 패키지 설치

```bash
pip install -r requirements.txt
```

설치되는 패키지:
- `flask` — 웹 서버
- `yt-dlp` — YouTube 영상 다운로드

> yt-dlp가 PATH에 등록되지 않아도 `python -m yt_dlp`로 자동 실행됩니다.

---

### 4. 서버 실행

```bash
python app.py
```

아래와 같은 메시지가 나오면 정상 실행된 것입니다:

```
 * Running on http://127.0.0.1:5000
```

---

### 5. 브라우저 접속

**Chrome 또는 Edge**에서 아래 주소로 접속합니다:

```
http://localhost:5000
```

---

## 사용 방법

### Step 1 — AI 모델 로드
- **"모델 로드"** 버튼 클릭
- 처음 실행 시 HuggingFace에서 약 **500MB** 다운로드 (2~5분 소요)
- 이후 브라우저 캐시에 저장되어 빠르게 로드됨
- 로그 창에 **"모델 준비 완료!"** 메시지가 뜨면 완료

### Step 2 — YouTube 영상 다운로드
- YouTube URL 입력란에 URL 붙여넣기
  예: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
- **"다운로드"** 버튼 클릭
- 로그 창에 "다운로드 완료" 메시지가 뜨면 영상이 플레이어에 로드됨

### Step 3 — 화면 분석
1. 영상 재생 후 분석하고 싶은 장면에서 **일시정지 (스페이스바)**
2. **"화면 분석"** 버튼 클릭
3. 로그 창에 **"분석 완료! XX초 소요"** 메시지가 뜨면 완료
4. 오른쪽 패널에 분석 결과(영어) 표시됨

---

## 프로젝트 구조

```
video-scene-analyzer/
├── app.py                # Flask 백엔드 (YouTube 다운로드 API)
├── requirements.txt      # Python 의존성 목록
├── README.md             # 이 파일
├── downloads/            # 다운로드된 영상 저장 폴더 (자동 생성)
└── templates/
    └── index.html        # 프론트엔드 (비디오 플레이어 + WebGPU AI 추론)
```

---

## 문제 해결

| 증상 | 해결 방법 |
|------|----------|
| 모델 로드 버튼이 반응 없음 | 페이지 새로고침 후 재시도 (Ctrl+Shift+R) |
| WebGPU 오류 | Chrome/Edge 113+ 사용 여부 확인. 자동으로 WASM 모드로 전환됨 |
| 영상 다운로드 실패 | yt-dlp 설치 확인: `python -m yt_dlp --version` |
| 분석 결과가 이상함 | Max Tokens를 128로 줄이거나 이미지 크기를 224px로 변경 후 재시도 |

---

## 주의사항

- WebGPU는 **Chrome 113+** 또는 **Edge**에서만 지원됩니다.
- 모델 첫 로드는 인터넷 속도에 따라 다르며 약 2~5분 소요됩니다.
- 화면 분석은 WebGPU 기준 약 **20~60초** 소요됩니다.
- WASM 모드(WebGPU 미지원 시)에서는 분석에 수 분 이상 소요될 수 있습니다.
