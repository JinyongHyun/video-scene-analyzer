# On-Device 영상 분석 앱

YouTube 영상을 다운로드하고, 정지 화면을 Qwen3.5 Vision (0.8B) 모델로 브라우저에서 직접 분석하는 웹 앱입니다.
모든 AI 추론은 **WebGPU**를 이용해 브라우저 내에서 로컬로 실행됩니다 (서버 전송 없음).

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| AI 모델 | `onnx-community/Qwen3.5-0.8B-ONNX` (HuggingFace) |
| 추론 환경 | Transformers.js v3.6.0 + WebGPU (q4 양자화) |
| 백엔드 | Python Flask + yt-dlp |
| 프레임 캡처 | Canvas API → RawImage (448×448) |

---

## 실행 방법

### 1. 사전 준비

- Python 3.8 이상
- Node.js 불필요 (순수 Python 백엔드)
- **브라우저**: Chrome 113+ 또는 Edge (WebGPU 지원 필요)
- **ffmpeg** (선택): 영상 병합에 사용. 없어도 단일 스트림으로 동작

### 2. 저장소 클론

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/homework2
```

### 3. Python 패키지 설치

```bash
pip install -r requirements.txt
```

> `yt-dlp`가 PATH에 없을 경우 `python -m yt_dlp`로 자동 실행됩니다.

### 4. 앱 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

---

## 사용 방법

1. **모델 로드** — "모델 로드 (~500MB)" 버튼 클릭
   - 처음 실행 시 약 500MB 다운로드 (이후 브라우저 캐시에 저장)
   - WebGPU 미지원 브라우저에서는 WASM으로 자동 폴백 (느림)

2. **영상 다운로드** — YouTube URL 입력 후 "다운로드" 클릭
   - 720p 이하로 자동 선택

3. **화면 분석** — 영상 재생 중 원하는 장면에서 일시정지 → "화면 분석" 클릭
   - 현재 프레임이 캡처되어 모델로 전달
   - 분석 결과가 한국어로 우측 패널에 표시

---

## 프로젝트 구조

```
homework2/
├── app.py                # Flask 백엔드 (YouTube 다운로드 API)
├── requirements.txt      # Python 의존성
├── README.md             # 이 파일
├── downloads/            # 다운로드된 영상 저장 (자동 생성)
└── templates/
    └── index.html        # 프론트엔드 (비디오 플레이어 + AI 추론)
```

---

## 주의사항

- WebGPU는 **Chrome 113+** 또는 **Edge**에서 지원됩니다.
- 모델 첫 로드 시 약 2~5분 소요될 수 있습니다.
- 분석 시간은 GPU 성능에 따라 다르며, WebGPU 기준 약 30~120초입니다.
