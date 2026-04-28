import os
import logging
import math
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------- CONFIG ----------------
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", "").strip()
if not TOKEN:
    raise Exception("TOKEN is missing in environment variables")

THRESHOLD = 50  # meters (distance to trigger alert)

user_locations = {}

# ---------------- DISTANCE FUNCTION ----------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# ---------------- TELEGRAM HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working. Send location 📍")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    user_locations[user_id] = (lat, lon)
    await update.message.reply_text("Location saved ✅")

    # check proximity with others
    for other_id, (olat, olon) in user_locations.items():
        if other_id != user_id:
            d = distance(lat, lon, olat, olon)

            if d <= THRESHOLD:
                msg = f"⚠️ You are near another user! Distance: {d:.1f} meters"

                await context.bot.send_message(chat_id=user_id, text=msg)
                await context.bot.send_message(chat_id=other_id, text=msg)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(user_locations) < 2:
        await update.message.reply_text("Need at least 2 users")
        return

    users = list(user_locations.keys())
    u1, u2 = users[0], users[1]

    lat1, lon1 = user_locations[u1]
    lat2, lon2 = user_locations[u2]

    d = distance(lat1, lon1, lat2, lon2)
    await update.message.reply_text(f"Distance: {d:.2f} meters")

# ---------------- FAKE WEB SERVER ----------------
def run_web():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Bot is running!"

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------------- MAIN ----------------
def main():
    # start web server (for Render)
    threading.Thread(target=run_web).start()

    # start telegram bot
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location))
    app.add_handler(CommandHandler("check", check))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
