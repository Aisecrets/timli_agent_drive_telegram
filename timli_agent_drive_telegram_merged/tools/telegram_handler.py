# tools/telegram_handler.py
from tools.telegram import send_telegram_message

def handle_telegram_update(update: dict) -> str:
    # Pak chat_id en tekst veilig uit het Telegram update-object
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    chat_id = str(chat.get("id") or "")
    text = (msg.get("text") or "").strip()

    if not chat_id:
        return "❌ geen chat_id gevonden"

    if not text:
        send_telegram_message(chat_id, "Ik heb je bericht ontvangen. Stuur tekst a.u.b.")
        return "ok"

    # Eenvoudig antwoord (echo) – dit is puur om te testen dat alles werkt
    send_telegram_message(chat_id, f"✅ Ontvangen: “{text}”")
    return "ok"
