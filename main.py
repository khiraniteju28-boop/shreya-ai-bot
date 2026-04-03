import telebot
from telebot import types
import os, datetime, threading, http.server, socketserver

# --- CONFIGURATION ---
API_TOKEN = '8685334276:AAH8Hpi9ooC8kY8R9d3ZiFY1bCulrvU3K18'
UPI_ID = 'khiranitejasvi-1@okhdfcbank'
QR_URL = 'https://raw.githubusercontent.com/khiraniteju28-boop/shreya-ai-bot/main/payment-qr.png'

bot = telebot.TeleBot(API_TOKEN)
used_utrs = set()
active_users = {} # {user_id: expiry_datetime}
pending_plans = {} # {user_id: selected_days}

# --- RENDER SERVER ---
def start_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()
threading.Thread(target=start_server, daemon=True).start()

# --- 🏠 1. START ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Get Started 🚀", callback_data="get_started"))
    bot.send_message(message.chat.id, "✨ *Mahi AI - Check voice for my channel*", reply_markup=markup, parse_mode='Markdown')

# --- 🛠️ 2. FLOW HANDLERS ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "get_started":
        bot.delete_message(chat_id, msg_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("By Using Shreya 🤖", callback_data="shreya"))
        bot.send_message(chat_id, "Welcome! Click below to continue.", reply_markup=markup)
    
    elif call.data == "shreya":
        bot.delete_message(chat_id, msg_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Agree ✅", callback_data="agree"))
        bot.send_message(chat_id, "Do you agree to terms and conditions?", reply_markup=markup)
    
    elif call.data == "agree":
        bot.delete_message(chat_id, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Indian Girl 🇮🇳", callback_data="voice_indian"),
                   types.InlineKeyboardButton("Japanese Girl 🇯🇵", callback_data="voice_japan"))
        bot.send_message(chat_id, "Choose Voice Style:", reply_markup=markup)

    elif "voice_" in call.data:
        bot.delete_message(chat_id, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⚡ 1 Day - ₹20", callback_data="buy_1"),
                   types.InlineKeyboardButton("🔋 5 Days - ₹60", callback_data="buy_5"),
                   types.InlineKeyboardButton("📅 1 Week - ₹300", callback_data="buy_7"),
                   types.InlineKeyboardButton("👑 1 Month - ₹800", callback_data="buy_30"))
        bot.send_message(chat_id, "🎙️ *Choose a Premium Plan:*", reply_markup=markup, parse_mode='Markdown')

    elif "buy_" in call.data:
        days = int(call.data.split("_")[1])
        pending_plans[chat_id] = days # Plan yaad rakho
        bot.delete_message(chat_id, msg_id)
        
        pay_msg = (f"💳 *Plan Selected: {days} Day(s)*\n\n"
                   f"1️⃣ QR Scan karein ya UPI: `{UPI_ID}`\n"
                   "2️⃣ Payment ke baad *12-digit UTR* yahan bhejein.\n\n"
                   "Bot turant aapka plan unlock kar dega!")
        bot.send_photo(chat_id, QR_URL, caption=pay_msg, parse_mode='Markdown')

# --- 🔍 3. AUTOMATIC VERIFICATION ---
@bot.message_handler(func=lambda message: len(message.text) == 12 and message.text.isdigit())
def verify_utr(message):
    utr = message.text
    user_id = message.from_user.id
    
    if utr in used_utrs:
        bot.reply_to(message, "❌ Ye UTR pehle use ho chuka hai!")
    elif user_id not in pending_plans:
        bot.reply_to(message, "❌ Pehle koi plan select karein!")
    else:
        used_utrs.add(utr)
        days = pending_plans[user_id]
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        active_users[user_id] = expiry
        
        bot.send_message(message.chat.id, 
                         f"✅ *Payment Verified!* \n\n"
                         f"🚀 Aapka {days} din ka plan unlock ho gaya hai!\n"
                         f"📅 Expiry: {expiry.strftime('%Y-%m-%d %H:%M')}\n\n"
                         "Ab aap voice bhejein, main convert kar dunga! ✨", parse_mode='Markdown')

# --- 🎙️ 4. VOICE CONVERSION (LOCK/UNLOCK) ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    now = datetime.datetime.now()
    
    if user_id in active_users and now < active_users[user_id]:
        bot.reply_to(message, "🎙️ *Voice Received!* \n\nConverting to Girl's Voice... Please wait. ⏳")
    else:
        bot.reply_to(message, "🔒 *Feature Locked!*\n\nAapka koi active plan nahi hai. /start dabayein.")

bot.polling(none_stop=True)
