# RevenantsRelayBot — Telegram ➜ Discord relay bot
import os
import requests
from flask import Flask, request

app = Flask(__name__)

DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
    # Add more topic-to-webhook mappings as needed
}

def get_webhook(topic_name):
    return DISCORD_WEBHOOKS.get(topic_name)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    topic = data.get("topic")
    text = data.get("text")
    username = data.get("username", "Unknown")
    avatar = data.get("avatar")

    webhook_url = get_webhook(topic)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

