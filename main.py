
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mappage des ID Telegram vers les Webhooks Discord
TELEGRAM_TO_DISCORD = {
    int(os.getenv("TELEGRAM_CHAT_ID_RU")): os.getenv("DISCORD_WEBHOOK_URL_RU"),
    int(os.getenv("TELEGRAM_CHAT_ID_TR")): os.getenv("DISCORD_WEBHOOK_URL_TR"),
}

# Mappage des hashtags vers les topics Discord
TOPIC_MAP = {
    "общий": "ru-general",
    "ru": "ru-general",
    "genel": "tr-general",
    "tr": "tr-general",
}


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    print(f">>> Données brutes reçues : {data}")

    if "message" in data:
        if "text" in data["message"]:
            text = data["message"]["text"]
            print(f">>> Texte reçu : {text}")
            words = text.strip().split()
            if not words:
                return "Aucun texte", 200

            hashtag = None
            if words[0].startswith("#"):
                hashtag = words[0][1:].lower()
            print(f">>> Hashtag extrait : {hashtag}")

            topic = TOPIC_MAP.get(hashtag)
            if not topic:
                print(f">>> Aucun topic trouvé pour : {hashtag}")
                return "Aucun topic associé", 200

            chat_id = data["message"]["chat"]["id"]
            webhook_url = TELEGRAM_TO_DISCORD.get(chat_id)
            if not webhook_url:
                print(f">>> Aucun webhook trouvé pour chat_id : {chat_id}")
                return "Aucun webhook associé", 200

            sender_name = data["message"]["from"]["first_name"]
            sender_username = data["message"]["from"].get("username", "")
            full_name = f"{sender_name} (@{sender_username})" if sender_username else sender_name

            content = " ".join(words[1:]) if hashtag else text

            payload = {
                "username": full_name,
                "content": content,
                "thread_name": topic
            }

            response = requests.post(webhook_url, json=payload)
            print(f">>> Requête envoyée à Discord, status : {response.status_code}")
            return "Message relayé", 200
        else:
            print(">>> Pas de texte dans le message")
            return "Pas de texte", 200
    else:
        print(">>> Pas de champ 'message'")
        return "Pas de message", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
