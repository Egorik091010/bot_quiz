import telebot
from config import TOKEN
from logic import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

bot = telebot.TeleBot(token=TOKEN)

SPORTS = ["Football", "Basketball", "Tennis", "Running", "Swimming"]
user_choices = {}

@bot.message_handler(commands=["go"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, Я бот который выберет твой любимый спорт,")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Напиши /start если хочешь начать" )

def send_question(chat_id):
    bot.send_message(chat_id, SPORTS[user_choices[chat_id]].text, reply_markup=SPORTS[user_choices[chat_id]].gen_markup())

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_choices[user_id] = []

    markup = InlineKeyboardMarkup(inline_keyboard=[])
    markup.row_width = len(self.options)
    
# Callback query handler for buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_selection(call: CallbackQuery):
    user_id = call.from_user.id
    data = call.data

    if user_id not in user_choices:
        user_choices[user_id] = []

    if data == "done":
        selected = user_choices[user_id]
        if not selected:
            bot.edit_message_text(
                "Ничего не выбрал 😅",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        else:
            top3 = selected[:3]
            text = "Твои топ 3 спорта:\n\n" + "\n".join(f"🏅 {sport}" for sport in top3)
            bot.edit_message_text(
                text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        return

    if data not in user_choices[user_id]:
        user_choices[user_id].append(data)
        bot.answer_callback_query(call.id, f"Added: {data}")
    else:
        bot.answer_callback_query(call.id, f"{data} already selected")

# Run the bot
bot.polling()