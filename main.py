from pathlib import Path

main_py_content = '''import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mapping des topics Telegram vers les webhooks Discord
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}

DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
}

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(">>> Données brutes reçues :", data)

    message = data.get("message")
    if not message:
        return "Aucun message", 400

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    # Extraction du topic depuis le hashtag
    topic = "inconnu"
    if "#" in text:
        topic = text.split("#")[-1].strip().lower()

    print(">>> Hashtag extrait :", topic)

    discord_channel = TOPIC_MAP.get(topic)
    if not discord_channel:
        return "Topic non pris en charge", 200

    webhook_url = DISCORD_WEBHOOKS.get(discord_channel)
    if not webhook_url:
        return "Webhook non défini", 500

    sender = message.get("from", {})
    sender_name = sender.get("first_name", "Anonyme")
    sender_username = sender.get("username", "")
    full_name = f"{sender_name} (@{sender_username})" if sender_username else sender_name

    discord_payload = {
        "username": full_name,
        "content": text,
    }

    response = requests.post(webhook_url, json=discord_payload)
    if response.status_code != 204:
        print("Erreur lors de l'envoi à Discord :", response.text)
        return "Erreur Discord", 500

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
'''

main_file_path = Path("/mnt/data/main.py")
main_file_path.write_text(main_py_content)

main_file_path
