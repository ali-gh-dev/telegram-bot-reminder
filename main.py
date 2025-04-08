# udemy course
import asyncio
import logging
import os
import threading
import time
import uuid

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import ConversationHandler, MessageHandler, filters

from memory_datasource import MemoryDataSource

# initial settings
load_dotenv()
TOKEN = os.getenv('my_token_2')
app = ApplicationBuilder().token(TOKEN).build()
# variables
ADD_REMINDER_TEXT = 'let\'s set a reminder ⏰'
SHOW_ALL_TEXT = '🗓 show all 🗓'
ENTER_MESSAGE, ENTER_TIME = range(2)
data_source = MemoryDataSource()
INTERVAL = 30
# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_btn = [[KeyboardButton(text=ADD_REMINDER_TEXT), KeyboardButton(text=SHOW_ALL_TEXT)]]
    markup = ReplyKeyboardMarkup(keyboard_btn, resize_keyboard=True)

    await update.message.reply_text("Hi dear user ...", reply_markup=markup)


async def add_reminder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == ADD_REMINDER_TEXT:
        await update.message.reply_text("Enter message of the reminder : ")
    elif user_choice == SHOW_ALL_TEXT:
        await update.message.reply_text("this section is under development ...")
        return
    return ENTER_MESSAGE


async def enter_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter time of the reminder :\n( like this ==> 25/01/2025 07:15 )\n ")
    context.user_data['reminder_text'] = update.message.text
    return ENTER_TIME


async def enter_time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_id = str(uuid.uuid4())
    reminder_text = context.user_data['reminder_text']
    reminder_time = update.message.text
    reminder = data_source.add_reminder(reminder_id=random_id,
                                        chat_id=update.message.chat_id,
                                        message=reminder_text,
                                        time=reminder_time)
    await update.message.reply_text(f"your reminder :\n===============\n{reminder}")
    # =============
    # this part is for testing :)
    # print('user_data : ', context.user_data)
    # print('dict of reminders : ', data_source.reminders)
    # =============
    return ConversationHandler.END


async def check_reminders():
    while True:
        print(f'{INTERVAL} seconds passed.')
        for reminder_id in data_source.reminders:
            reminder = data_source.reminders[reminder_id]
            if reminder.should_be_fired():
                reminder.fire()

                await app.bot.send_message(chat_id=reminder.chat_id,
                                           text=f"👇👇👇 it\'s time. 👇👇👇\n{reminder.message}")

        time.sleep(INTERVAL)


def wrapped_async_check_reminders():
    asyncio.run(check_reminders())


def start_checking_reminders():
    print("thread started ...")
    thread = threading.Thread(target=wrapped_async_check_reminders, args=())
    thread.daemon = True
    thread.start()


def main():
    print('======= The Bot started working =======')

    # commands
    app.add_handler(CommandHandler('start', start_handler))

    # conversation
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(f"^({ADD_REMINDER_TEXT}|{SHOW_ALL_TEXT})$"), add_reminder_handler)],
        states={
            ENTER_MESSAGE: [MessageHandler(filters.ALL, enter_message_handler)],
            ENTER_TIME: [MessageHandler(filters.ALL, enter_time_handler)]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)

    # tip : this function must be called before app.run_polling()
    start_checking_reminders()

    app.run_polling()


if __name__ == '__main__':
    main()
