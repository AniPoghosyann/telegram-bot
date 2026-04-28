import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import math

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN missing in environment variables")

user_locations = {}

def distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send location 📍")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    user_locations[user_id] = (lat, lon)
    await update.message.reply_text("Saved ✅")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(user_locations) < 2:
        await update.message.reply_text("Need 2 users")
        return

    users = list(user_locations.keys())
    u1, u2 = users[0], users[1]

    lat1, lon1 = user_locations[u1]
    lat2, lon2 = user_locations[u2]

    d = distance(lat1, lon1, lat2, lon2)

    await update.message.reply_text(f"Distance: {d:.2f} meters")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()

if __name__ == "__main__":
    main()
