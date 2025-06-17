import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DISCORD_WEBHOOKS = {
    "ru-general": os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    "tr-general": os.getenv("DISCORD_WEBHOOK_TR_GENERAL"),
}

TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}

def extract_hashtag(text):
    if not text:
        return None
    for word in text.split():
        if word.startswith("#"):
            return word[1:].lower()
    return None

def send_to_discord(webhook_url, content, username=None, avatar_url=None):
    data = {"content": content}
    if username:
        data["username"] = username
    if avatar_url:
        data["avatar_url"] = avatar_url
    response = requests.post(webhook_url, json=data)
    return response.status_code == 204

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    print(f">>> Données brutes reçues : {data}")

    message = data.get("message")
    if not message:
        return "No message", 400

    chat = message.get("chat", {})
    if chat.get("type") != "supergroup":
        return "Not a supergroup", 400

    text = message.get("text", "")
    hashtag = extract_hashtag(text)
    print(f">>> Hashtag extrait : {hashtag}")

    topic_key = chat.get("title", "").split("-")[-1].lower()
    topic_id = TOPIC_MAP.get(topic_key)

    if not topic_id:
        print(">>> Aucun topic trouvé pour :", topic_key)
        return "No topic found", 400

    webhook_url = DISCORD_WEBHOOKS.get(topic_id)
    if not webhook_url:
        print(">>> Aucun webhook configuré pour :", topic_id)
        return "No webhook", 400

    sender = message.get("from", {})
    username = sender.get("first_name", "Anon")
    avatar_url = f"https://t.me/i/userpic/320/{sender.get('username')}.jpg" if sender.get("username") else None

    send_to_discord(webhook_url, text, username=username, avatar_url=avatar_url)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
