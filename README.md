# 📢 Advertiser Bot — Telegram Advertising Automation (Python)

A Telegram bot built with **Python** designed to automate sending promotional messages inside Telegram groups where the bot is a member.  
Users running the bot locally can submit a message and define how many times it should be broadcast.

---

## 🚀 Features

### 📩 Group-Based Advertising
- Sends promotional messages to all Telegram groups where the bot has access  
- Controlled and sequential message sending  
- Avoids spam-like behavior by managing repetition count

### 🧑‍💻 User Interaction
Users can:
- Enter a promotional message  
- Specify the number of times the message should be sent  
- Trigger the broadcast using simple commands

### ⚙️ Message Dispatch Logic
- Handles repeated sending based on user input  
- Can be extended with cooldowns or scheduling  
- Works with multiple groups automatically

### 💰 Planned Monetization (Not Implemented Yet)
The architecture is prepared for:
- Pay-per-message  
- Pay-per-campaign  
- User credit system  
- Billing history and usage tracking  

*(This part is under development.)*

---

## 🧰 Tech Stack
- **Python**
- **python-telegram-bot** (or your specific library—update if needed)
- Standard Python modules

---

## 🔧 Configuration (config.data)

Bot configuration is stored inside a file named **`config.data`**:

---

## ▶️ Running the Bot

1. Install dependencies:

```bash
pip install
```

Run the bot:
```
python bot.py
```

🎯 Purpose of This Project
	•	Demonstrates Telegram bot automation
	•	Simple advertising/broadcasting mechanism
	•	Clean separation between configuration and bot logic
	•	Extensible design for future paid advertising system

A practical portfolio project showing Python automation skills.

⸻

✨ Author

Behzad Mehrabi
Software Developer — Python • Automation • Bots • .NET • JavaScript


