
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Correspondance directe entre ID de groupe Telegram et webhook Discord
TELEGRAM_TO_DISCORD = {
    int(os.getenv("TELEGRAM_CHAT_ID_RU")): os.getenv("DISCORD_WEBHOOK_RU_GENERAL"),
    int(os.getenv("TELEGRAM_CHAT_ID_TR")): os.getenv("DISCORD_WEBHOOK_TR_GENERAL")
}

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    print(f">>> Données brutes reçues : {data}")

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        username = message['from']['username'] if 'from' in message and 'username' in message['from'] else "Inconnu"

        if 'text' in message:
            text = message['text']
            print(f">>> Texte reçu : {text}")

            # Envoi direct sans hashtag
            webhook_url = TELEGRAM_TO_DISCORD.get(chat_id)
            if webhook_url:
                print(f">>> Chat ID reconnu : {chat_id}")
                print(f">>> Envoi à Discord via : {webhook_url}")

                payload = {
                    "username": f"[TG] {username}",
                    "content": text
                }

                response = requests.post(webhook_url, json=payload)
                print(f">>> Statut Discord : {response.status_code}")
                return "OK", 200
            else:
                print(f">>> Chat ID inconnu : {chat_id}")
                return "Chat ID non autorisé", 403
        else:
            print(">>> Aucun texte trouvé dans le message.")
            return "Pas de texte", 400
    else:
        print(">>> Structure inattendue : pas de champ 'message'")
        return "Mauvais format", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
