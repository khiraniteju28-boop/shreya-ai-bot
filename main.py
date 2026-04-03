import telebot
from telebot import types
import time

# Aapka Token
TOKEN = '8693684961:AAFS_FSIT-YXERUQbRKY1vHF65rl_qTkr7s'
bot = telebot.TeleBot(TOKEN)

# Aapki IDs
VOICE_ID = 'CQACAgUAAxkBAAMEac9GSP_qhGjfciUVWyRWgZQlWrIAAvkyAAJnbXlWNLMfgqGS2eE6BA'
QR_ID = 'AgACAgUAAxkBAAMFac9GWRbB7EM7vIURPtuv-TBW3iEAAr8NaxtnbXlWZOt8lXnDAx4BAAMCAAN5AAM6BA'

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🚀 Get Started / Shuru Karein", callback_data="get_started")
    markup.add(btn)
    welcome_text = (
        "👋 **Welcome to Sanu AI Service**\n\n"
        "Main aapki voice AI assistant hoon. Mere paas behad real sounding voices hain jo aapke kaam aa sakti hain.\n\n"
        "📢 **Demo sunne ke liye niche button dabayein!**"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_started":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("✅ I Agree / Mujhe Manzoor Hai", callback_data="agree")
        markup.add(btn)
        bot.send_message(call.message.chat.id, "⚠️ **Terms & Conditions**\n\nIs bot ko use karke aap hamari AI policy se sehmat hote hain.", parse_mode="Markdown", reply_markup=markup)

    elif call.data == "agree":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🎧 Indian Girl Voice (Demo)", callback_data="voice_indian")
        markup.add(btn1)
        bot.send_message(call.message.chat.id, "✨ **Voice Selection**\n\nNiche button dabakar meri awaaz ka sample suniye:", reply_markup=markup)

    elif call.data == "voice_indian":
        bot.send_voice(call.message.chat.id, VOICE_ID)
        time.sleep(1) # Thoda gap taaki user audio sun sake
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("💎 View Premium Plans", callback_data="show_plans")
        markup.add(btn)
        bot.send_message(call.message.chat.id, "Awaaz kaisi lagi? Kya aap full access chahte hain?", reply_markup=markup)

    elif call.data == "show_plans":
        # Yahan humne har button ko alag line mein rakha hai (row_width=1)
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        btn1 = types.InlineKeyboardButton("🔥 Unlimited Voice - ₹45", callback_data="buy_plan")
        btn2 = types.InlineKeyboardButton("🌟 All Voice Models - ₹50", callback_data="buy_plan")
        btn3 = types.InlineKeyboardButton("⚡ 1 Day Trial Plan - ₹20", callback_data="buy_plan")
        
        markup.add(btn1, btn2, btn3)
        
        plan_text = (
            "💰 **Sanu AI Premium Plans**\n\n"
            "Aap apni pasand ka plan chuniye:\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **Unlimited Voice:** Sab kuch unlimited (₹45)\n"
            "2️⃣ **All Models:** Saare AI characters (₹50)\n"
            "3️⃣ **1 Day Plan:** Aaj ke liye trial (₹20)\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(call.message.chat.id, plan_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy_plan":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("✅ Yes, Pay Now", callback_data="show_qr")
        markup.add(btn)
        bot.send_message(call.message.chat.id, "Kya aap payment karne ke liye taiyaar hain?", reply_markup=markup)

    elif call.data == "show_qr":
        bot.send_photo(call.message.chat.id, QR_ID, 
                       caption="📸 **Payment Details**\n\n1. Scan karein aur pay karein.\n2. **Screenshot** yahan zaroori bhejein.\n\nAapka access 5 min mein chalu ho jayega! 🚀", 
                       parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()
if __name__ == "__main__":
    print("Sanu AI Bot is Starting...")
    bot.remove_webhook() # Ye line zaroori hai conflict hatane ke liye
    bot.infinity_polling()
