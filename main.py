import telebot
from telebot import types
import datetime

# --- CONFIGURATION ---
API_TOKEN = '8685334276:AAH8H-y_fQy7-Z_S0'
UPI_ID = 'khiranitejasvi-1@okhdfcbank'
# Ye link tabhi chalega jab GitHub par photo upload hogi
QR_URL = 'https://raw.githubusercontent.com/khiraniteju28-boop/shreya-ai-bot/main/payment-qr.png'

bot = telebot.TeleBot(API_TOKEN)
active_users = {} 
pending_plans = {} 

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Get Started 🚀", callback_data="get_started"))
    bot.send_message(message.chat.id, "✨ *Mahi AI - Voice Conversion Bot*", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if call.data == "get_started":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("By Using Shreya 🤖", callback_data="shreya"))
        bot.send_message(chat_id, "Aage badhne ke liye niche click karein:", reply_markup=markup)
    elif call.data == "shreya":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Agree ✅", callback_data="agree"))
        bot.send_message(chat_id, "Kya aap terms se sahmat hain?", reply_markup=markup)
    elif call.data == "agree":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Indian Girl 🇮🇳", callback_data="v_in"),
                   types.InlineKeyboardButton("Japanese Girl 🇯🇵", callback_data="v_jp"))
        bot.send_message(chat_id, "Voice Style select karein:", reply_markup=markup)
    elif "v_" in call.data:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⚡ 1 Day - ₹20", callback_data="buy_1"),
                   types.InlineKeyboardButton("🔋 5 Days - ₹60", callback_data="buy_5"),
                   types.InlineKeyboardButton("📅 1 Week - ₹300", callback_data="buy_7"),
                   types.InlineKeyboardButton("👑 1 Month - ₹800", callback_data="buy_30"))
        bot.send_message(chat_id, "🎙️ *Plan select karein:*", reply_markup=markup, parse_mode='Markdown')
    elif "buy_" in call.data:
        days = int(call.data.split("_")[1])
        pending_plans[chat_id] = days
        pay_msg = (f"💳 *Plan: {days} Din Selected*\n\n"
                   f"1️⃣ QR Scan karein ya UPI: `{UPI_ID}`\n"
                   "2️⃣ Payment ke baad *12-digit UTR* yahan likhein.\n\n"
                   "Bot turant check karke plan chalu kar dega! ✅")
        bot.send_photo(chat_id, QR_URL, caption=pay_msg)

@bot.message_handler(func=lambda message: len(message.text) == 12 and message.text.isdigit())
def verify_utr(message):
    user_id = message.from_user.id
    if user_id in pending_plans:
        days = pending_plans[user_id]
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        active_users[user_id] = expiry
        bot.send_message(user_id, f"✅ *UTR Received!* \n\nAapka plan {days} din ke liye active ho gaya hai. \n\nValid tak: {expiry.strftime('%Y-%m-%d %H:%M')}\nAb voice bhejiye! ✨")
    else:
        bot.send_message(user_id, "❌ Pehle plan select karein.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    if user_id in active_users and datetime.datetime.now() < active_users[user_id]:
        bot.reply_to(message, "🎙️ *Voice Mil Gayi!* \nAI convert kar raha hai... thoda wait karein. ⏳")
    else:
        bot.reply_to(message, "🔒 *Locked!* Aapka koi active plan nahi hai. /start karke plan lein.")

bot.polling(none_stop=True)
