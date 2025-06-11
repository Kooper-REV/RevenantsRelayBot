import os
import requests
from flask import Flask, request

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Association des IDs de topic Telegram avec les clés internes des webhooks
TOPIC_MAP = {
    "101": "ru-general",  # Remplace ces IDs par ceux affichés dans les logs
    "102": "tr-general",
}

# Récupération des webhooks Discord depuis les variables d’environnement
DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
}

def get_webhook(topic_id):
    internal_key = TOPIC_MAP.get(topic_id)
    return DISCORD_WEBHOOKS.get(internal_key)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    print(">>> Données brutes reçues :", data)  # 💡 nouvelle ligne

    message = data.get("message")
    if not message:
        return "No message field", 400

    text = message.get("text", "")
    username = message["from"].get("username", "Unknown")
    avatar = None

    topic_id = str(message.get("message_thread_id", ""))
    print(">>> Topic ID reçu :", topic_id)  # 👈 Affiche l’ID brut

    topic_name = TOPIC_MAP.get(topic_id, "inconnu")

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
