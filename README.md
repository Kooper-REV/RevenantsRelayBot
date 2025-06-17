# RevenantsRelayBot

Bidirectional relay bot between **Telegram** and **Discord**, created for the multilingual community **Revenants**.

This bot synchronizes text messages between specific **Telegram groups** and **Discord channels**, with support for:

* **Usernames and avatars**
* **Language-based group-to-channel mapping**
* **Auto-translation via RITA (on Discord side only)**

---

## 🌐 Use Case

Designed for communities managing multi-language chat:

* Telegram Groups (🇷🇺 Russian, 🇹🇷 Turkish)
* Discord Channels in corresponding languages
* Full Telegram ➔ Discord message relay

---

## 🔧 Features

* ✅ Telegram ➔ Discord: Sends Telegram messages to Discord via webhooks
* ✅ Avatar and name sync from Telegram
* ✅ Maps messages per group to matching Discord channel
* ✅ Easily extensible
* ⚙️ Optional translation with [RITA](https://discord.bots.gg/bots/706406664205623316) on Discord

---

## 🚀 Deployment

The bot is designed to run on **Render** or **Railway** for permanent uptime without local hosting.

### Files provided:

* `main.py`: Telegram ➔ Discord relay based on group origin
* `requirements.txt`: Python dependencies
* `.env.example`: Sample environment file

Your `.env` file should include:

```env
DISCORD_WEBHOOK_RU_GENERAL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_TR_GENERAL=https://discord.com/api/webhooks/...
TELEGRAM_RU_CHAT_ID=-1001234567890
TELEGRAM_TR_CHAT_ID=-1009876543210
```

---

## 📜 License

[MIT License](LICENSE)

---

## 🛠️ Group Mapping

In `main.py`, Telegram chat IDs are matched like so:

```python
GROUP_MAP = {
    os.getenv("TELEGRAM_RU_CHAT_ID"): "ru-general",
    os.getenv("TELEGRAM_TR_CHAT_ID"): "tr-general",
}
```

---

## ✅ Example Message Flow

**From Telegram group 🇷🇺:**

```
Привет!
```

Goes ➔ `#ru-general` on Discord with same username

**From Telegram group 🇹🇷:**

```
Selam!
```

Goes ➔ `#tr-general` on Discord with same username
