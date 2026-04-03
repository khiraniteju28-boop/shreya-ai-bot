import telebot
from telebot import types
import os, datetime, threading, http.server, socketserver

# --- CONFIGURATION ---
API_TOKEN = '8685334276:AAH8Hpi9ooC8kY8R9d3ZiFY1bCulrvU3K18'
UPI_ID = 'khiranitejasvi-1@okhdfcbank'
# Aapka upload kiya hua QR image link
QR_URL = 'https://raw.githubusercontent.com/khiraniteju28-boop/shreya-ai-bot/main/payment-qr.png'

bot = telebot.TeleBot(API_TOKEN)
used_utrs = set()
active_users = {} 

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

# --- 🛠️ 2. STEP-BY-STEP FLOW (No extra messages) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "get_started":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("By Using Shreya 🤖", callback_data="shreya"))
        bot.edit_message_text("Welcome! Click below to continue.", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "shreya":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Agree ✅", callback_data="agree"))
        bot.edit_message_text("Do you agree to terms and conditions?", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "agree":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Indian Girl 🇮🇳", callback_data="voice_indian"),
                   types.InlineKeyboardButton("Japanese Girl 🇯🇵", callback_data="voice_japan"))
        bot.edit_message_text("Choose Voice Style:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif "voice_" in call.data:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⚡ 1 Day - ₹20", callback_data="buy_20"),
                   types.InlineKeyboardButton("🔋 5 Days - ₹60", callback_data="buy_60"),
                   types.InlineKeyboardButton("📅 1 Week - ₹300", callback_data="buy_300"),
                   types.InlineKeyboardButton("👑 Unlimited - ₹800", callback_data="buy_800"))
        # Yahan humne demo link hata diya hai
        bot.edit_message_text("🎙️ *Voice Style Selected.*\n\nChoose a Premium Plan to start Voice Conversion:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

    elif "buy_" in call.data:
        amount = call.data.split("_")[1]
        # Pehle purana message delete karenge taaki saaf dikhe
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        payment_text = (f"💳 *Plan Selected: ₹{amount}*\n\n"
                        f"1️⃣ QR Code scan karein ya UPI ID copy karein: `{UPI_ID}`\n"
                        "2️⃣ Payment ke baad *12-digit UTR* number yahan likhein.\n\n"
                        "Bot turant verify karke plan chalu kar dega! ✅")
        bot.send_photo(call.message.chat.id, QR_URL, caption=payment_text, parse_mode='Markdown')

# --- 🔍 3. UTR VERIFICATION ---
@bot.message_handler(func=lambda message: len(message.text) == 12 and message.text.isdigit())
def verify_utr(message):
    utr = message.text
    user_id = message.from_user.id
    
    if utr in used_utrs:
        bot.reply_to(message, "❌ Ye UTR pehle use ho chuka hai!")
    else:
        used_utrs.add(utr)
        # Default 1 day activation
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        active_users[user_id] = expiry
        bot.send_message(message.chat.id, f"✅ *Payment Verified!* \nAapka plan active ho gaya hai. Ab voice message bhejiye! ✨", parse_mode='Markdown')

# --- 🎙️ 4. VOICE LOCK/UNLOCK ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    now = datetime.datetime.now()
    
    if user_id in active_users and now < active_users[user_id]:
        bot.reply_to(message, "🎙️ Voice Received! Converting to Girl's Voice... ⏳")
    else:
        bot.reply_to(message, "🔒 *Feature Locked!* \nKripya /start dabakar plan lein aur UTR bhej kar unlock karein.")

bot.polling(none_stop=True)
