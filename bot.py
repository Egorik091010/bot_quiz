import telebot
from config import TOKEN
from logic import *
from telegram import CallbackQuery
from logic import SPORT


bot = telebot.TeleBot(token=TOKEN)
user_choices = {}

@bot.message_handler(commands=["go"])
def go(message):
    bot.send_message(message.chat.id, f"Привет, Я бот который выберет твой любимый спорт,")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Напиши /start если хочешь начать" )



@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_choices[chat_id] = []

    question = SPORT(
        "Выбери 3 любимые виды спорта:",
        *SPORT.SPORTS
    )
    bot.send_message(chat_id, question.text, reply_markup=question.gen_markup())
        


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
