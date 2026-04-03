import telebot
from telebot import types
import os, datetime, threading, http.server, socketserver

# --- CONFIGURATION ---
API_TOKEN = '8685334276:AAH8H-y_fQy7-Z_S0' # Aapka Mahi AI Token
bot = telebot.TeleBot(API_TOKEN)

# Database (Temporary memory for UTR and Active Users)
used_utrs = set()
active_users = {} # {user_id: expiry_time}

# --- RENDER SERVER (Free Plan Fix) ---
def start_server():
    port = int(os.environ.get("PORT", 8080))
    server = socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler)
    server.serve_forever()
threading.Thread(target=start_server, daemon=True).start()

# --- STEP 1: WELCOME & PLANS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⚡ 1 Day Plan - ₹20", callback_data="buy_20"),
        types.InlineKeyboardButton("🎤 Unlimited Voice - ₹45", callback_data="buy_45"),
        types.InlineKeyboardButton("🎭 All Voice Models - ₹50", callback_data="buy_50")
    )
    bot.send_message(message.chat.id, 
                     "✨ *Mahi AI Premium Models* ✨\n\n"
                     "Ladki ki awaz (RVC) use karne ke liye plan chuniye:", 
                     reply_markup=markup, parse_mode='Markdown')

# --- STEP 2: QR & PAYMENT INSTRUCTION ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_payment(call):
    plan_price = call.data.split("_")[1]
    msg = (f"💳 *Plan: ₹{plan_price}*\n\n"
           "1️⃣ Niche diye QR par payment karein (Ya UPI: `aapki@upi`)\n"
           "2️⃣ Payment ke baad *12-digit UTR Number* yahan bhejein.\n\n"
           "⚠️ *Note:* UTR daalte hi feature automatic unlock ho jayega!")
    bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')

# --- STEP 3: AUTOMATIC UTR VERIFICATION & UNLOCK ---
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
                         "Ab aap apni *Voice Message* bhejein, main use convert kar dunga! 🎙️")

# --- STEP 4: VOICE CONVERSION (LOCK/UNLOCK LOGIC) ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    now = datetime.datetime.now()
    
    # Check if user has active plan
    if user_id in active_users and now < active_users[user_id]:
        bot.reply_to(message, "🎙️ *Voice Received!* \n\nConverting to Girl's Voice... Please wait. ⏳")
        # Yahan RVC/ElevenLabs processing connect hogi
    else:
        bot.reply_to(message, "🔒 *Feature Locked!*\n\nYe feature sirf paid users ke liye hai. Kripya /start dabakar plan lein.")

bot.polling(none_stop=True)
        
