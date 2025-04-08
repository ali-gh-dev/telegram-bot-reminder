# udemy course
import logging
import os
from dotenv import load_dotenv
import uuid
from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup
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

    app.run_polling()


if __name__ == '__main__':
    main()
