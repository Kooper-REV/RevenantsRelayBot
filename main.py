import os
import requests
from flask import Flask, request

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Association des topics Telegram avec les clés internes des webhooks
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}

# Récupération des webhooks Discord depuis les variables d’environnement
DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
}

def get_webhook(topic_name):
    internal_key = TOPIC_MAP.get(topic_name)
    return DISCORD_WEBHOOKS.get(internal_key)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json

    message = data.get("message")
    if not message:
        return "No message field", 400

    text = message.get("text", "")
    username = message["from"].get("username", "Unknown")
    avatar = None  # Telegram doesn't provide avatar by default

    topic_name = None
    if "message_thread_id" in message:
        topic_name = message.get("forum_topic", {}).get("name")
    else:
        topic_name = "общий"  # fallback si aucun topic n’est envoyé

    webhook_url = get_webhook(topic_name)
    if not webhook_url:
        return f"No matching webhook for topic '{topic_name}'", 400

    payload = {
        "username": username,
        "content": text,
    }
    if avatar:
        payload["avatar_url"] = avatar

    requests.post(webhook_url, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
