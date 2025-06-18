
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Mapping des groupes Telegram vers les webhooks Discord
TELEGRAM_TO_DISCORD = {
    int(os.getenv("TELEGRAM_CHAT_ID_RU")): os.getenv("DISCORD_WEBHOOK_URL_RU"),
    int(os.getenv("TELEGRAM_CHAT_ID_TR")): os.getenv("DISCORD_WEBHOOK_URL_TR"),
}

@app.route("/telegram", methods=["POST"])
def handle_telegram():
    data = request.json
    print(">>> Données brutes reçues :", data)

    # Vérifie que c'est un message avec texte
    if not data.get("message"):
        print(">>> Pas de champ 'message' détecté")
        return "No message", 200

    if "text" not in data["message"]:
        print(">>> Message reçu sans texte")
        return "No text", 200

    print(f">>> Texte reçu : {data['message']['text']}")

    chat_id = data["message"]["chat"]["id"]
    username = data["message"]["from"].get("username", "Unknown")
    text = data["message"]["text"]

    webhook_url = TELEGRAM_TO_DISCORD.get(chat_id)

    if not webhook_url:
        print(f">>> Aucun webhook trouvé pour chat_id : {chat_id}")
        return "Unknown chat", 200

    payload = {
        "username": username,
        "content": text,
    }

    response = requests.post(webhook_url, json=payload)
    print(f">>> Envoi vers Discord : status {response.status_code} | payload : {payload}")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
