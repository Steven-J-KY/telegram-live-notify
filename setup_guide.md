# 🚀 빠른 시작 가이드

5 분 안에 설정 완료!

## 1️⃣ 텔레그램 봇 만들기 (1 분)

1. Telegram 앱에서 [@BotFather](https://t.me/botfather) 검색 → 대화 시작
2. `/newbot` 입력
3. 봇 이름 입력 (예: `MyYouTubeLiveBot`)
4. 봇 토큰 복사 (예: `1234567890:ABCdef...`)

## 2️⃣ Chat ID 확인 (30 초)

1. [@userinfobot](https://t.me/userinfobot) 검색 → 대화 시작
2. 자동으로 Chat ID 표시 (예: `123456789`)
3. 이 숫자 복사

## 3️⃣ YouTube API 키 발급 (2 분)

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. **새 프로젝트 생성** → 프로젝트 이름 입력
3. **API 및 서비스** → **YouTube Data API v3** 검색 → **활성화**
4. **사용 인증 정보** → **API 키 만들기** → **API 키 복사**

## 4️⃣ 채널 ID 확인 (1 분)

1. 유튜브 채널 페이지 접속 (예: `https://www.youtube.com/@ChannelName`)
2. URL 이 `youtube.com/channel/UCxxxxx...` 형태라면 그 부분 복사
3. 또는 우클릭 → 페이지 소스 보기 → `"channelId":"UCxxxxx..."` 검색

## 5️⃣ 코드 설정 (1 분)

`telegram_bot.py` 파일 열어서 아래 4 개 줄만 수정:

```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # 1️⃣에서 복사
TELEGRAM_CHAT_ID = "123456789"  # 2️⃣에서 복사
YOUTUBE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX"  # 3️⃣에서 복사

YOUTUBE_CHANNEL_IDS = [
    "UCxxxxxxxxxxxxxxxxxxx",  # 4️⃣에서 복사한 채널 ID
]
```

## 6️⃣ 실행 (30 초)

```bash
# 의존성 설치
pip install -r requirements.txt

# 봇 실행
python telegram_bot.py
```

## ✅ 완료!

이제 지정한 유튜브 채널에서 라이브 방송이 시작되면 텔레그램으로 알림이 갑니다!

---

## 🧪 테스트

테스트 알림을 보내보고 싶다면:

```python
# telegram_bot.py 하단의 main() 함수에서 아래 줄 주석 해제:
bot.test_notification()
```

그리고 다시 `python telegram_bot.py` 실행!

## ⚠️ 주의

- `.env` 파일이나 코드에 API 키를 GitHub 에 올리지 마세요!
- YouTube API 는 일일 쿼터 제한이 있습니다 (기본 10,000 단위)
- `CHECK_INTERVAL` 을 300 초 (5 분) 이상으로 설정하는 것을 권장합니다
