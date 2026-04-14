import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

import requests


SIGN_URL = os.environ.get("TWO_LIBRA_SIGN_URL", "https://2libra.com/api/sign")
TIMEOUT = int(os.environ.get("TWO_LIBRA_TIMEOUT", "20"))
COOKIE_FILE = Path(__file__).with_name("2libra_cookie.txt")

SUCCESS_KEYWORDS = (
    "签到成功",
    "今天已经签到过了",
    "已签到",
    "签到勤勉检定",
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("2libra_checkin")


def build_headers(cookie: str) -> dict:
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Origin": "https://2libra.com",
        "Referer": "https://2libra.com/",
        "Cookie": cookie,
    }


def load_cookie() -> str:
    if not COOKIE_FILE.exists():
        logger.error("Cookie file not found: %s", COOKIE_FILE)
        return ""

    cookie = COOKIE_FILE.read_text(encoding="utf-8").strip()
    if not cookie:
        logger.error("Cookie file is empty: %s", COOKIE_FILE)
        return ""

    return cookie


def parse_response(response: requests.Response) -> tuple[bool, str]:
    text = response.text.strip()

    try:
        payload = response.json()
    except ValueError:
        payload = None

    if payload is not None:
        normalized = json.dumps(payload, ensure_ascii=False)
        for keyword in SUCCESS_KEYWORDS:
            if keyword in normalized:
                return True, normalized

        if response.status_code in (200, 201):
            if payload.get("success") is True:
                return True, normalized
            if payload.get("code") in (0, 200, 201):
                return True, normalized

    for keyword in SUCCESS_KEYWORDS:
        if keyword in text:
            return True, text

    if response.status_code == 201:
        return True, text or "HTTP 201"

    return False, text or f"HTTP {response.status_code}"


def check_in() -> int:
    cookie = load_cookie()
    if not cookie:
        return 2

    headers = build_headers(cookie)
    started_at = datetime.now()
    logger.info("Sending sign request to %s", SIGN_URL)

    try:
        response = requests.post(SIGN_URL, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as exc:
        logger.error("Request failed: %s", exc)
        return 1

    ok, detail = parse_response(response)
    elapsed = (datetime.now() - started_at).total_seconds()

    logger.info("HTTP %s, elapsed %.2fs", response.status_code, elapsed)

    if ok:
        logger.info("Check-in succeeded: %s", detail[:500])
        return 0

    logger.error("Check-in failed: %s", detail[:500])
    return 1


if __name__ == "__main__":
    sys.exit(check_in())
