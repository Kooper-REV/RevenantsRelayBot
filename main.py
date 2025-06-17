import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(**name**)

# Mapping entre les hashtags et les noms internes de salons

TOPIC\_MAP = {
"общий": "ru-general",
"genel": "tr-general",
}

# Webhooks Discord associés

DISCORD\_WEBHOOKS = {
"ru-general": os.getenv("DISCORD\_WEBHOOK\_RU\_GENERAL"),
"tr-general": os.getenv("DISCORD\_WEBHOOK\_TR\_GENERAL"),
}

def get\_webhook(topic\_name):
internal\_key = TOPIC\_MAP.get(topic\_name)
return DISCORD\_WEBHOOKS.get(internal\_key)

@app.route('/telegram', methods=\['POST'])
def telegram\_webhook():
data = request.json
print(">>> Données brutes reçues :", data)

```
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
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=10000)
