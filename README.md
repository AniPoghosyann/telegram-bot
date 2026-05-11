# Telegram-Bot

## Architecture

```text
Telegram Bot
    ↓
User Location Messages
    ↓
In-Memory Storage (Python dict)
    ↓
Haversine Distance Calculation
    ↓
Proximity Detection Engine
    ↓
Instant Telegram Alerts
    ↓
Flask Web Server (Render / VPS Keep-Alive)
```

---

## Short Description

Tracks users’ live locations in Telegram and detects when two users come close to each other.

If the distance between users is less than a defined threshold (default: 50 meters), the bot immediately sends a warning message to both users.

---

## Features

- Telegram bot interface  
- Real-time location tracking  
- Automatic proximity detection  
- Haversine formula-based distance calculation  
- Instant alert system between users  
- Flask web server for deployment (Render / VPS keep-alive)  
- Supports multiple simultaneous users  
- Lightweight in-memory storage (no database required)  

---

## Usage

After installation, run the Telegram bot:

```bash
python your_file_name.py
```

---

## How to use the bot

1. Open Telegram and start your bot  
2. Send:

```text
/start
```

3. Share your live location  
4. The bot automatically stores and compares user positions  

---

## What happens next

- Bot receives user location updates  
- Stores coordinates in memory  
- Continuously calculates distance between users  
- If distance < threshold (e.g. 50m), both users get an alert  
- Flask server keeps bot alive on hosting platforms  

---

## Notes

- Users must enable location sharing in Telegram  
- In-memory storage resets when server restarts  
- Best used with Flask keep-alive (Render / VPS / Replit)  
