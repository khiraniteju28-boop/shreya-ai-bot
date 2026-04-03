import telebot
from telebot import types
import os, datetime, threading, http.server, socketserver, requests

# --- 🛠️ CONFIGURATION ---
# Aapka Mahi AI Token (Jo aapne screenshot mein dikhaya tha)
API_TOKEN = '8685334276:AAH8H-y_fQy7-Z_S0'
bot = telebot.TeleBot(API_TOKEN)

# Database (Temporary memory for UTR and Active Users)
used_utrs = set()
active_users = {} # {user_id: expiry_time}

# --- 🌐 RENDER DUMMY SERVER (Free Plan Fix) ---
def start_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()
threading.Thread(target=start_server, daemon=True).start()

# --- 🏠 STEP 1: WELCOME & PLANS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("⚡ 1 Day Plan - ₹20", callback_data="buy_20")
    btn2 = types.InlineKeyboardButton("🎤 Unlimited Voice - ₹45", callback_data="buy_45")
    btn3 = types.InlineKeyboardButton("🎭 All Voice Models - ₹50", callback_data="buy_50")
    btn4 = types.InlineKeyboardButton("📸 AI Influencer Guide", callback_data="ai_guide")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 
                     "✨ *Mahi AI Premium Models* ✨\n\n"
                     "Ladki ki awaz (RVC) aur AI Models ke liye niche se plan chuniye:", 
                     reply_markup=markup, parse_mode='Markdown')

# --- 💳 STEP 2: PAYMENT & UTR INSTRUCTION ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_payment(call):
    plan_price = call.data.split("_")[1]
    payment_msg = (f"💳 *Plan Selected: ₹{plan_price}*\n\n"
                   "1️⃣ Niche diye gaye QR par payment karein.\n"
                   "2️⃣ Payment ke baad apna *12-digit UTR Number* yahan message mein bhejein.\n\n"
                   "Bot turant aapka plan 24 ghante ke liye activate kar dega! ✅")
    bot.send_message(call.message.chat.id, payment_msg, parse_mode='Markdown')

# --- 🔍 STEP 3: AUTOMATIC UTR VERIFICATION & UNLOCK ---
@bot.message_handler(func=lambda message: len(message.text) == 12 and message.text.isdigit())
def verify_payment(message):
    utr = message.text
    user_id = message.from_user.id
    
    if utr in used_utrs:
        bot.reply_to(message, "❌ Ye UTR pehle use ho chuka hai!")
    else:
        # UTR ko save kar lo taaki dubara use na ho
        used_utrs.add(utr)
        
        # 24 Hours ke liye access dena
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        active_users[user_id] = expiry
        
        bot.send_message(message.chat.id, 
                         f"✅ *Payment Verified!* (UTR: {utr})\n\n"
                         f"🚀 Aapka plan active ho gaya hai!\n"
                         f"📅 Expiry: {expiry.strftime('%Y-%m-%d %H:%M')}\n\n"
                         "Ab aap apni *Voice Message* bhejein, main use convert kar dunga! 🎙️",
                         parse_mode='Markdown')

# --- 🎙️ STEP 4: VOICE CONVERSION (LOCK/UNLOCK LOGIC) ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    now = datetime.datetime.now()
    
    # Check if user has active plan
    if user_id in active_users and now < active_users[user_id]:
        bot.reply_to(message, "🎙️ *Voice Received!* \n\nConverting to Girl's Voice... Please wait. ⏳")
        # Yahan RVC/ElevenLabs API call connect hoga
    else:
        bot.reply_to(message, "🔒 *Feature Locked!*\n\nYe feature sirf paid users ke liye hai. Kripya /start dabakar plan lein.")

bot.polling(none_stop=True)
