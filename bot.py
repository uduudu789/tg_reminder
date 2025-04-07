from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time
import pytz
import logging
import os

# === Configuration ===
#BOT_TOKEN = os.getenv("BOT_TOKEN")
#CHAT_ID = os.getenv("CHAT_ID")  # Used for reminders
#logging.info(f"Loaded BOT_TOKEN: {'yes' if BOT_TOKEN else 'no'}")
#logging.info(f"Loaded CHAT_ID: {CHAT_ID}")
#if not BOT_TOKEN or not CHAT_ID:
#    raise ValueError("❌ Missing BOT_TOKEN or CHAT_ID environment variable")


BOT_TOKEN = '7878395503:AAFNhJcoOaGs-rYlt3UyBmTElzGe9ngGUDI'
CHAT_ID = 72831350

# === Load environment variables ===
#BOT_TOKEN = os.getenv("BOT_TOKEN")
#CHAT_ID = os.getenv("CHAT_ID")
logging.info(f"Loaded BOT_TOKEN: {'yes' if os.getenv("BOT_TOKEN") else 'no'}")
logging.info(f"Loaded CHAT_ID: {CHAT_ID}")
print("BOT_TOKEN is:", os.getenv("BOT_TOKEN"))
print("CHAT_ID is:", os.getenv("CHAT_ID"))

YOUR_ID = CHAT_ID  # Use this for command responses

TIMEZONE = pytz.timezone("Etc/GMT-3")  # = GMT+3, see note below

REMINDERS = [
    ("🧼 Wash knives", time(17, 55)),
    ("🧼 Wash knives", time(22, 55)),
    ("🧼 Wash knives", time(21, 55)),
    ("🥕 Check vegetables", time(18, 30)),
    ("🥕 Check vegetables", time(17, 50)),
    ("📝 Check the shopping list", time(21, 45)),
    ("📝 Check the shopping list", time(16, 0)),
    ("📝 Check the shopping list", time(17, 0)),
    ("🍽️ Cook dinner", time(18, 0)),
    ("🧽 Wash the kitchen after dinner", time(21, 25)),
    ("👕 Hang out the laundry", time(16, 45)),
    ("👕 Hang out the laundry", time(18, 20)),
    ("👕 Hang out the laundry", time(13, 25)),
    ("👕 Hang out the laundry", time(12, 25)),
    ("🛁 Tidy up the bathroom", time(11, 0)),
    ("🛁 Tidy up the bathroom", time(12, 20)),
    ("🛁 Tidy up the bathroom", time(13, 25)),
    ("🛏️ Tidy up the table and nightstand", time(21, 30)),
]

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Bot Setup ===
bot = Bot(BOT_TOKEN)
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
scheduler = BackgroundScheduler(timezone=TIMEZONE)

# === Reminder Job ===
def send_reminder(message):
    def job():
        logger.info(f"Sending reminder: {message}")
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Done", callback_data=f"done:{message}")
        ]])
        bot.send_message(chat_id=CHAT_ID, text=message, reply_markup=keyboard)
    return job

def handle_done(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # acknowledge click

    if query.data.startswith("done:"):
        logger.info(f"Marked done: {query.data[5:]}")
        try:
            context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")


for message, reminder_time in REMINDERS:
    scheduler.add_job(
        send_reminder(message),
        'cron',
        hour=reminder_time.hour,
        minute=reminder_time.minute
    )

# === Start Command ===
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == YOUR_ID:
        context.bot.send_message(chat_id=user_id, text="👋 Hello! Your reminder bot is up and running.")
    else:
        context.bot.send_message(chat_id=user_id, text="⛔ Sorry, this bot is private.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(handle_done))

# === Start Bot ===
scheduler.start()
updater.start_polling()
logger.info("Bot started.")
updater.idle()
