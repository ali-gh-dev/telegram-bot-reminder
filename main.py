# udemy course
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

# initial settings
load_dotenv()
TOKEN = os.getenv('my_token_2')
app = ApplicationBuilder().token(TOKEN).build()
ADD_REMINDER_TEXT = 'let\'s set a reminder ⏰'
SHOW_ALL_TEXT = '🗓 show all 🗓'
# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_btn = [[KeyboardButton(text=ADD_REMINDER_TEXT), KeyboardButton(text=SHOW_ALL_TEXT)]]
    markup = ReplyKeyboardMarkup(keyboard_btn, resize_keyboard=True)

    await update.message.reply_text("Hi dear user ...", reply_markup=markup)


def main():
    print('======= The Bot started working =======')

    # commands
    app.add_handler(CommandHandler('start', start))

    app.run_polling()


if __name__ == '__main__':
    main()
