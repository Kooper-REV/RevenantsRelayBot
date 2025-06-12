import sys
import os
import requests
from flask import Flask, request

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Mapping entre les hashtags et les noms internes de salons
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}

# Webhooks Discord associés
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
    print(">>> Données brutes reçues :", data)

    message = data.get("message")
    if not message:
        return "No message field", 400

    text = message.get("text", "")
    username = message["from"].get("username", "Unknown")
    avatar = None

    topic_name = "inconnu"

    if "#" in text:
        words = text.split()
        for word in words:
            if word.startswith("#"):
                topic_name = word.lstrip("#").lower()
                break

    print(">>> Hashtag extrait :", topic_name)

    webhook_url = get_webhook(topic_name)
    if not webhook_url:
        return f"No matching webhook for topic '{topic_name}'", 400

    payload = {
        "username": username,
        "content": text,
    }
    if avatar:
        payload["avatar_url"] = avatar

    print(">>> Webhook utilisé :", webhook_url)
    print(">>> Contenu envoyé :", payload)

    requests.post(webhook_url, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
