# tools/diag.py
import os

def check_env():
    """Controleer of TELEGRAM_BOT_TOKEN aanwezig is."""
    tok = os.getenv("TELEGRAM_BOT_TOKEN")
    return "OK token set" if tok else "MISSING TELEGRAM_BOT_TOKEN"

def parse_update(update: dict):
    """
    Haal chat_id en text uit een Telegram update.
    Handig om te zien of je webhook payload correct is.
    """
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    chat_id = str(chat.get("id") or "")
    text = (msg.get("text") or "").strip()
    return {"chat_id": chat_id, "text": text, "has_chat_id": bool(chat_id), "has_text": bool(text)}

def test_send(chat_id: str):
    """Stuur testbericht via tools.telegram.send_telegram_message."""
    from tools.telegram import send_telegram_message
    return send_telegram_message(chat_id, "Diag ping ✅ via Leap")
