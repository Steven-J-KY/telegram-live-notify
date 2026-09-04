#!/usr/bin/env python3
"""
YouTube Live Notification Bot
유튜브 라이브 방송 시작 시 텔레그램으로 알림을 전송하는 봇
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional, Set, Dict, Any
from dataclasses import dataclass, field

import requests
from telegram import Bot
from telegram.error import TelegramError

# ==================== 설정 ====================

# 환경 변수로 설정 (권장) 또는 직접 입력
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")

# 모니터링할 유튜브 채널 ID 목록 (채널 ID 또는 @username)
YOUTUBE_CHANNEL_IDS = [
    "UCxxxxxxxxxxxxxxxxxxx",  # 예시: 채널 ID
    # 추가 채널들은 여기에 추가
]

# 확인 주기 (초) - YouTube API 쿼터 제한 고려 (기본: 300 초 = 5 분)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("youtube_live_bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class LiveStream:
    """라이브 스트림 정보"""
    video_id: str
    title: str
    channel_title: str
    thumbnail_url: str
    live_url: str
    started_at: Optional[str] = None
    viewer_count: Optional[int] = None
    notified: bool = False


class YouTubeLiveMonitor:
    """유튜브 라이브 스트림 모니터링 클래스"""

    def __init__(self, api_key: str, channel_ids: list):
        self.api_key = api_key
        self.channel_ids = channel_ids
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.notified_streams: Set[str] = set()
        self.all_streams: Dict[str, LiveStream] = {}

    def get_live_streams(self) -> list[LiveStream]:
        """현재 라이브 중인 스트림 목록 조회"""
        live_streams = []

        for channel_id in self.channel_ids:
            try:
                # Search API 를 사용해 현재 라이브 중인 영상 검색
                search_url = f"{self.base_url}/search"
                params = {
                    "part": "snippet",
                    "channelId": channel_id,
                    "eventType": "live",
                    "type": "video",
                    "key": self.api_key,
                    "maxResults": 5,  # 채널당 최대 5 개까지 확인
                    "fields": "items(id/videoId,snippet/title,snippet/channelTitle,snippet/thumbnails/default/url)"
                }

                response = requests.get(search_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                for item in data.get("items", []):
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]

                    stream = LiveStream(
                        video_id=video_id,
                        title=snippet["title"],
                        channel_title=snippet["channelTitle"],
                        thumbnail_url=snippet["thumbnails"]["default"]["url"],
                        live_url=f"https://www.youtube.com/watch?v={video_id}"
                    )

                    # 상세 정보 조회 (시작 시간, 시청자 수 등)
                    self._enrich_stream_info(stream)
                    live_streams.append(stream)

            except requests.exceptions.RequestException as e:
                logger.error(f"API 요청 오류 (채널 {channel_id}): {e}")
            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

        return live_streams

    def _enrich_stream_info(self, stream: LiveStream) -> None:
        """스트림 상세 정보 조회 (Video API)"""
        try:
            video_url = f"{self.base_url}/videos"
            params = {
                "part": "liveStreamingDetails,statistics",
                "id": stream.video_id,
                "key": self.api_key,
                "fields": "items(liveStreamingDetails/actualStartTime,statistics/viewerCount)"
            }

            response = requests.get(video_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("items"):
                item = data["items"][0]
                live_details = item.get("liveStreamingDetails", {})
                stats = item.get("statistics", {})

                stream.started_at = live_details.get("actualStartTime")
                stream.viewer_count = int(stats.get("viewerCount", 0))

        except Exception as e:
            logger.warning(f"상세 정보 조회 실패 ({stream.video_id}): {e}")

    def check_new_streams(self) -> list[LiveStream]:
        """새로운 라이브 스트림 감지"""
        current_streams = self.get_live_streams()
        new_streams = []

        for stream in current_streams:
            if stream.video_id not in self.notified_streams:
                # 이전에 알림을 보낸 적 없는 새 스트림
                new_streams.append(stream)
                self.notified_streams.add(stream.video_id)
                logger.info(f"새 라이브 감지: {stream.title} ({stream.video_id})")
            else:
                logger.debug(f"이미 알림된 스트림: {stream.title}")

        # 종료된 스트림은 추적에서 제거 (선택적)
        current_ids = {s.video_id for s in current_streams}
        self.notified_streams = self.notified_streams.intersection(current_ids)

        return new_streams


class TelegramNotifier:
    """텔레그램 알림 전송 클래스"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)

    def send_live_notification(self, stream: LiveStream) -> bool:
        """라이브 시작 알림 전송"""
        message = self._format_message(stream)

        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=False
            )
            logger.info(f"알림 전송 완료: {stream.video_id}")
            return True

        except TelegramError as e:
            logger.error(f"텔레그램 전송 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"알림 전송 중 오류: {e}")
            return False

    def _format_message(self, stream: LiveStream) -> str:
        """알림 메시지 포맷팅"""
        viewer_text = ""
        if stream.viewer_count is not None:
            viewer_text = f"👥 시청자: {stream.viewer_count:,}명\n"

        time_text = ""
        if stream.started_at:
            try:
                started_dt = datetime.fromisoformat(stream.started_at.replace("Z", "+00:00"))
                kst_dt = started_dt.astimezone()
                time_text = f"🕐 시작: {kst_dt.strftime('%Y-%m-%d %H:%M:%S')} KST\n"
            except Exception:
                pass

        message = (
            f"🔴 <b>라이브 방송 시작!</b>\n\n"
            f"📺 <b>{self._escape_html(stream.title)}</b>\n"
            f"🎬 채널: {self._escape_html(stream.channel_title)}\n"
            f"{viewer_text}"
            f"{time_text}"
            f"🔗 <a href=\"{stream.live_url}\">바로보기</a>\n\n"
            f"#유튜브 #라이브 #알림"
        )

        return message

    @staticmethod
    def _escape_html(text: str) -> str:
        """HTML 특수문자 이스케이프"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


class LiveNotificationBot:
    """메인 봇 클래스"""

    def __init__(self):
        self.monitor = YouTubeLiveMonitor(YOUTUBE_API_KEY, YOUTUBE_CHANNEL_IDS)
        self.notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.running = False

    def run(self) -> None:
        """봇 실행 (무한 루프)"""
        logger.info("YouTube Live Notification Bot 시작")
        logger.info(f"모니터링 채널: {len(YOUTUBE_CHANNEL_IDS)}개")
        logger.info(f"확인 주기: {CHECK_INTERVAL}초")

        self.running = True

        try:
            while self.running:
                new_streams = self.monitor.check_new_streams()

                for stream in new_streams:
                    success = self.notifier.send_live_notification(stream)
                    if success:
                        stream.notified = True

                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("사용자 요청으로 종료")
        except Exception as e:
            logger.error(f"봇 실행 중 치명적 오류: {e}")
            raise
        finally:
            self.running = False
            logger.info("Bot 종료")

    def test_notification(self) -> None:
        """테스트 알림 전송"""
        test_stream = LiveStream(
            video_id="TEST_VIDEO_ID",
            title="🧪 테스트 알림 - YouTube Live Bot",
            channel_title="Test Channel",
            thumbnail_url="",
            live_url="https://www.youtube.com/",
            viewer_count=0
        )

        logger.info("테스트 알림 전송...")
        success = self.notifier.send_live_notification(test_stream)

        if success:
            logger.info("✅ 테스트 알림 전송 성공!")
        else:
            logger.error("❌ 테스트 알림 전송 실패")


def main():
    """메인 함수"""
    # 설정 검증
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.error("TELEGRAM_BOT_TOKEN 이 설정되지 않았습니다.")
        logger.error("환경 변수를 설정하거나 코드에서 직접 입력하세요.")
        return

    if TELEGRAM_CHAT_ID == "YOUR_CHAT_ID":
        logger.error("TELEGRAM_CHAT_ID 가 설정되지 않았습니다.")
        logger.error("환경 변수를 설정하거나 코드에서 직접 입력하세요.")
        return

    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
        logger.error("YOUTUBE_API_KEY 가 설정되지 않았습니다.")
        logger.error("환경 변수를 설정하거나 코드에서 직접 입력하세요.")
        return

    if not YOUTUBE_CHANNEL_IDS or YOUTUBE_CHANNEL_IDS[0] == "UCxxxxxxxxxxxxxxxxxxx":
        logger.error("YOUTUBE_CHANNEL_IDS 에 유효한 채널 ID 를 입력하세요.")
        return

    # 봇 인스턴스 생성 및 실행
    bot = LiveNotificationBot()

    # 테스트 모드 (선택적)
    # bot.test_notification()

    # 실제 실행
    bot.run()


if __name__ == "__main__":
    main()
