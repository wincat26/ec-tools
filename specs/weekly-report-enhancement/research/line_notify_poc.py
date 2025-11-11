"""
LINE Messaging API push message PoC.

Usage:
    1. Export environment variables (see README section below).
    2. Run: python line_notify_poc.py --text "週報推播測試"
       or   python line_notify_poc.py --flex flex_payload.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"


def load_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"[ERROR] Environment variable {name} is not set.", file=sys.stderr)
        sys.exit(1)
    return value


def send_push_message(token: str, to: str, messages: list[dict]) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"to": to, "messages": messages}

    response = requests.post(LINE_PUSH_ENDPOINT, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        print("✅ Push message success.")
    else:
        print(f"❌ Push failed: {response.status_code} {response.text}", file=sys.stderr)
        response.raise_for_status()


def build_text_message(text: str) -> list[dict]:
    return [{"type": "text", "text": text}]


def build_flex_message(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        flex_content = json.load(f)
    return [
        {
            "type": "flex",
            "altText": flex_content.get("altText", "Weekly report"),
            "contents": flex_content["contents"],
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="LINE Messaging API push PoC")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text message to send")
    group.add_argument("--flex", help="Path to Flex message JSON file")
    parser.add_argument("--target", help="Override LINE target ID (user/group). Defaults to env LINE_TARGET_ID.")
    args = parser.parse_args()

    access_token = load_env("LINE_CHANNEL_ACCESS_TOKEN")
    target = args.target or load_env("LINE_TARGET_ID")

    if args.text:
        messages = build_text_message(args.text)
    else:
        messages = build_flex_message(Path(args.flex).resolve())

    send_push_message(access_token, target, messages)


if __name__ == "__main__":
    main()

