import os
import requests
from typing import Optional

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_BASE = os.getenv("TELEGRAM_API_BASE", "https://api.telegram.org")

def send_telegram_message(chat_id: str, text: str, parse_mode: Optional[str] = None) -> str:
    """
    Stuur een bericht via de Telegram Bot API.
    Returns: "ok" of een foutstring (begint met ❌).
    """
    token = TELEGRAM_BOT_TOKEN
    if not token:
        return "❌ TELEGRAM_BOT_TOKEN ontbreekt"

    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.ok:
            return "ok"
        return f"❌ Telegram API {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Telegram request error: {e}"
