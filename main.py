import telebot
from telebot import types
import time

# Aapka Final Token
TOKEN = '8693684961:AAFS_FSIT-YXERUQbRKY1vHF65rl_qTkr7s'
bot = telebot.TeleBot(TOKEN)

# Aapki IDs jo Penguin se nikaali thin
VOICE_ID = 'CQACAgUAAxkBAAMEac9GSP_qhGjfciUVWyRWgZQlWrIAAvkyAAJnbXlWNLMfgqGS2eE6BA'
QR_ID = 'AgACAgUAAxkBAAMFac9GWRbB7EM7vIURPtuv-TBW3iEAAr8NaxtnbXlWZOt8lXnDAx4BAAMCAAN5AAM6BA'

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Get Started", callback_data="get_started"))
    bot.send_message(message.chat.id, "Welcome to Sanu AI\n\nCheck voice for my channel", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_started":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Agree", callback_data="agree"))
        bot.send_message(call.message.chat.id, "Let's Get Started with Sanu AI\n\n*Note: By using AI you agree to our terms*", parse_mode="Markdown", reply_markup=markup)

    elif call.data == "agree":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Indian Girl 🇮🇳", callback_data="voice_indian"))
        bot.send_message(call.message.chat.id, "Kya aap hamari voice demo check karna chahoge?\nChoose your voice model:", reply_markup=markup)

    elif call.data == "voice_indian":
        bot.send_voice(call.message.chat.id, VOICE_ID)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Yes", callback_data="show_plans"))
        bot.send_message(call.message.chat.id, "Kya aap hamara plan choose karna chahoge?", reply_markup=markup)

    elif call.data == "show_plans":
        # Yahan humne buttons ko ek ke niche ek kar diya hai taaki price na kate
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💎 Unlimited Voice - ₹45", callback_data="buy_plan")
        btn2 = types.InlineKeyboardButton("📥 10 Download - ₹10", callback_data="buy_plan")
        btn3 = types.InlineKeyboardButton("🎧 20 All Voice Models - ₹20", callback_data="buy_plan")
        btn4 = types.InlineKeyboardButton("📞 Call Support - ₹50", callback_data="buy_plan")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(call.message.chat.id, "Choose a plan:", reply_markup=markup)

    elif call.data == "buy_plan":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Yes", callback_data="show_qr"))
        bot.send_message(call.message.chat.id, "When you buy?", reply_markup=markup)

    elif call.data == "show_qr":
        bot.send_photo(call.message.chat.id, QR_ID, caption="QR valid for 5 minutes.\n\n*Payment ke baad screenshot zaroori bhejein*", parse_mode="Markdown")

if __name__ == "__main__":
    print("Sanu AI Bot is Starting...")
    bot.infinity_polling()
