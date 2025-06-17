import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mapping des hashtags vers les topics Discord
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}

# Mapping des Chat IDs Telegram vers les Webhooks Discord
CHAT_ID_TO_WEBHOOK = {
    int(os.getenv("TELEGRAM_CHAT_ID_RU")): os.getenv("DISCORD_WEBHOOK_URL_RU"),
    int(os.getenv("TELEGRAM_CHAT_ID_TR")): os.getenv("DISCORD_WEBHOOK_URL_TR"),
}


def extraire_hashtag(texte):
    mots = texte.split()
    for mot in mots:
        if mot.startswith("#"):
            return mot[1:].lower()
    return None


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(f">>> Données brutes reçues : {data}")

    if 'message' in data:
        if 'text' in data['message']:
            print(f">>> Texte reçu : {data['message']['text']}")
            texte = data['message']['text']
            pseudo = data['message']['from']['first_name']
            avatar_url = f"https://t.me/i/userpic/320/{data['message']['from']['id']}.jpg"

            hashtag = extraire_hashtag(texte)
            print(f">>> Hashtag extrait : {hashtag}")

            if hashtag:
                topic = TOPIC_MAP.get(hashtag)
                if topic:
                    chat_id = data['message']['chat']['id']
                    webhook_url = CHAT_ID_TO_WEBHOOK.get(chat_id)

                    if webhook_url:
                        payload = {
                            "username": pseudo,
                            "avatar_url": avatar_url,
                            "content": texte,
                            "thread_name": topic
                        }
                        response = requests.post(webhook_url, json=payload)
                        print(f">>> Réponse Discord : {response.status_code} {response.text}")
                    else:
                        print(f">>> Aucun webhook défini pour le chat_id : {chat_id}")
                else:
                    print(f">>> Aucun topic trouvé pour : {hashtag}")
            else:
                print(">>> Aucun hashtag détecté dans le message.")
    return "", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
