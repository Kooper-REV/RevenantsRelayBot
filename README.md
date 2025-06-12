# RevenantsRelayBot

Bidirectional relay bot between **Telegram** and **Discord**, created for the multilingual community **Revenants**.

This bot synchronizes text messages between specific topics in Telegram groups and matching channels on Discord, with support for:

* **Usernames and avatars**
* **Language-based group/topic management**
* **Auto-translation via RITA (on Discord side only)**

---

## 🌐 Use Case

Designed for communities managing multi-language groups:

* Telegram Groups with Topics (e.g., 🇷🇺 Russian, 🇹🇷 Turkish)
* Discord Channels in different languages
* Cross-platform visibility of messages while keeping native features on each platform

---

## 🔧 Features

* ✅ Telegram ➔ Discord: Sends Telegram messages to Discord via webhooks
* ✅ Discord ➔ Telegram: Forwards Discord messages to Telegram using a bot account
* ✅ Avatar and name sync from Telegram
* ✅ Works with multiple topics/channels
* ✅ Easily extensible
* ⚙️ Optional translation with [RITA](https://discord.bots.gg/bots/706406664205623316) on Discord

---

## 🚀 Deployment

The bot is designed to run on **Render** or **Railway** for permanent uptime without local hosting.

### Files provided:

* `main.py`: Working relay bot (Telegram ➔ Discord), supports custom topic names via hashtags
* `requirements.txt`: Python dependencies
* `.env.example`: Example environment configuration file

---

## 📜 License

[MIT License](LICENSE)

---

## 🤝 Acknowledgements

Built by KOOPER with ❤️ for the Revenants LifeAfter Community.

---

## 🛠️ Topic Mapping Support

Now includes hashtag-based topic-to-webhook mapping. Messages must include a **#hashtag** (e.g. `#общий`) corresponding to the internal webhook name (e.g. `ru-general`).

In `main.py`, ensure `TOPIC_MAP` contains:

```python
TOPIC_MAP = {
    "общий": "ru-general",
    "genel": "tr-general",
}
```

So a Telegram message like:

```
#общий Salut !
```

Will relay to the Discord webhook for `ru-general`.
