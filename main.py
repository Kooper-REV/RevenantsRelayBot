import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mapping entre les noms visibles dans Telegram et les noms internes
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
    # Ajoute d'autres topics ici si besoin
}

DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
    # Ajoute d’autres clés si tu en as
}

def get_webhook_from_topic(telegram_topic):
    key = TOPIC_MAP.get(telegram_topic)
    return DISCORD_WEBHOOKS.get(key)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    topic = data.get("topic")
    text = data.get("text")
    username = data.get("username", "Unknown")
    avatar = data.get("avatar", None)

    webhook_url = get_webhook_from_topic(topic)
    if not webhook_url:
        return "No matching webhook", 400

    payload = {
        "username": username,
        "content": text,
    }

    if avatar:
        payload["avatar_url"] = avatar

    requests.post(webhook_url, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
