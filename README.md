# 📺 YouTube Live Notification Bot

유튜브 라이브 방송이 시작되면 텔레그램으로 자동 알림을 보내는 Python 봇입니다.

## ✨ 기능

- 🔴 유튜브 채널의 라이브 방송 시작 자동 감지
- 📱 텔레그램으로 실시간 알림 전송
- 🔄 다중 채널 모니터링 지원
- ⏰ 사용자 정의 확인 주기 설정
- 📊 시청자 수, 시작 시간 등 상세 정보 포함
- 🛡️ 중복 알림 방지 로직 내장

## 📋 사전 준비

### 1. 텔레그램 봇 토큰 발급

1. Telegram 에서 [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령어 입력
3. 봇 이름 설정 (예: `YouTubeLiveBot`)
4. 봇 토큰 복사 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. 텔레그램 Chat ID 확인

1. 텔레그램에서 [@userinfobot](https://t.me/userinfobot) 또는 [@getmyid_bot](https://t.me/getmyid_bot) 검색
2. 봇과 대화 시작
3. Chat ID 확인 (예: `123456789`)

### 3. YouTube Data API 키 발급

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스** → **YouTube Data API v3** 활성화
4. **사용 인증 정보** → **API 키 만들기**
5. 생성된 API 키 복사

### 4. 유튜브 채널 ID 확인

1. 유튜브 채널 페이지 접속
2. URL 에서 채널 ID 추출:
   - `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxx` → `UCxxxxxxxxxxxxxxxxxxx`
   - 또는 [Channel ID Finder](https://commentpicker.com/youtube-channel-id.php) 사용

## 🚀 설치 및 실행

### 1. 저장소 클론 또는 파일 다운로드

```bash
git clone https://github.com/Steven-J-KY/telegram-live-notify.git
cd telegram-live-notify
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 설정 (두 가지 방법)

#### 방법 A: 환경 변수 사용 (권장)

```bash
# Linux/macOS
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
export YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
export CHECK_INTERVAL="300"

# Windows (PowerShell)
$env:TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
$env:TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
$env:YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
$env:CHECK_INTERVAL="300"
```

#### 방법 B: 코드 직접 수정

`telegram_bot.py` 파일의 상단 설정 부분 수정:

```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID = "123456789"
YOUTUBE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX"

YOUTUBE_CHANNEL_IDS = [
    "UCxxxxxxxxxxxxxxxxxxx",  # 모니터링할 채널 ID
    "UCyyyyyyyyyyyyyyyyyyy",  # 추가 채널
]
```

### 4. 봇 실행

```bash
python telegram_bot.py
```

## 📁 파일 구조

```
telegram-live-notify/
├── telegram_bot.py       # 메인 봇 코드
├── requirements.txt      # Python 의존성
├── README.md            # 사용 가이드
└── youtube_live_bot.log  # 실행 로그 (자동 생성)
```

## ⚙️ 설정 옵션

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 토큰 | 필수 |
| `TELEGRAM_CHAT_ID` | 알림을 받을 Chat ID | 필수 |
| `YOUTUBE_API_KEY` | YouTube Data API 키 | 필수 |
| `YOUTUBE_CHANNEL_IDS` | 모니터링할 채널 ID 목록 | 필수 |
| `CHECK_INTERVAL` | 방송 확인 주기 (초) | 300 (5 분) |

## 🔧 고급 설정

### API 쿼터 관리

YouTube Data API 는 일일 쿼터 제한이 있습니다 (기본 10,000 단위).

- `search.list` 호출: 100 단위
- `CHECK_INTERVAL=300` (5 분) → 시간당 12 회 → 채널 1 개당 하루 288 회
- **권장**: 5~10 분 간격으로 설정

### 다중 채널 모니터링

```python
YOUTUBE_CHANNEL_IDS = [
    "UCxxxxxxxxxxxxxxxxxxx",  # 채널 1
    "UCyyyyyyyyyyyyyyyyyyy",  # 채널 2
    "UCzzzzzzzzzzzzzzzzzz",   # 채널 3
]
```

### 로깅 레벨 변경

```python
logging.basicConfig(
    level=logging.DEBUG,  # INFO → DEBUG 로 변경
    ...
)
```

## 🐳 Docker 로 실행 (선택)

### Dockerfile 생성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_bot.py .

CMD ["python", "telegram_bot.py"]
```

### 빌드 및 실행

```bash
docker build -t youtube-live-bot .
docker run -d \
  -e TELEGRAM_BOT_TOKEN="YOUR_TOKEN" \
  -e TELEGRAM_CHAT_ID="YOUR_CHAT_ID" \
  -e YOUTUBE_API_KEY="YOUR_API_KEY" \
  --name youtube-bot \
  youtube-live-bot
```

## 🧪 테스트 모드

코드 하단의 주석을 해제하면 테스트 알림을 보낼 수 있습니다:

```python
# bot.test_notification()  # 이 줄의 주석 해제
```

## 📝 알림 메시지 예시

```
🔴 라이브 방송 시작!

📺 [방송 제목]
🎬 채널: [채널명]
👥 시청자: 1,234 명
🕐 시작: 2026-09-05 02:30:00 KST
🔗 바로보기

#유튜브 #라이브 #알림
```

## ⚠️ 주의사항

1. **API 쿼터 제한**: YouTube Data API 는 일일 사용량 제한이 있습니다
2. **봇 보안**: API 키와 토큰은 절대 GitHub 에 공개하지 마세요
3. **채널 ID**: 채널 핸들 (@username) 이 아닌 실제 채널 ID(UC 로 시작) 를 사용하세요
4. **로그 파일**: `youtube_live_bot.log` 파일이 자동으로 생성됩니다

## 🛠️ 문제 해결

### "API 요청 오류" 발생

- API 키가 올바른지 확인
- YouTube Data API 가 활성화되었는지 확인
- API 쿼터 한도를 초과하지 않았는지 확인

### "텔레그램 전송 오류" 발생

- 봇 토큰이 올바른지 확인
- Chat ID 가 숫자형식인지 확인
- 봇이 사용자와 대화한 적이 있는지 확인 (첫 메시지는 사용자가 먼저)

### 라이브를 감지하지 못함

- 채널이 실제로 라이브 중인지 확인
- 채널 ID 가 올바른지 확인
- 확인 주기 (`CHECK_INTERVAL`) 를 줄여보세요

## 📄 라이선스

MIT License

## 🤝 기여

이슈 및 PR 환영합니다!

---

**제작**: Steven_Jin_KY  
**저장소**: https://github.com/Steven-J-KY/telegram-live-notify
