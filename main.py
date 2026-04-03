import telebot
from telebot import types

# Yahan apna Telegram Bot Token daalein (Jo BotFather se mila tha)
API_TOKEN = 'YAHAN_APNA_TOKEN_DALIYE'

bot = telebot.TeleBot(API_TOKEN)

# Jab koi /start likhe
@bot.message_code_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # Aapke Store ke Buttons
    btn1 = types.KeyboardButton('🛍️ Mishu Store')
    btn2 = types.KeyboardButton('👗 Clothes Collection')
    btn3 = types.KeyboardButton('🎨 Crafts & Arts')
    btn4 = types.KeyboardButton('📞 Contact Us')
    
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        "✨ **Welcome to Sanu AI!** ✨\n\n"
        "Aapka swagat hai hamare digital store mein.\n"
        "Niche diye gaye buttons ka use karke hamara collection dekhein."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode='Markdown')

# Buttons par click karne par kya hoga
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == '🛍️ Mishu Store':
        bot.reply_to(message, "Hamara Mishu Store jald hi live hone wala hai! Stay tuned.")
    
    elif message.text == '👗 Clothes Collection':
        bot.reply_to(message, "👗 Trending Kapde:\n1. Saree\n2. Kurtis\n3. Kids Wear\n\nOrder ke liye message karein.")
        
    elif message.text == '🎨 Crafts & Arts':
        bot.reply_to(message, "🎨 Handmade Items:\n1. Home Decor\n2. Gift Items\n\nUnique crafts yahan milenge.")
        
    elif message.text == '📞 Contact Us':
        bot.reply_to(message, "Hamein contact karne ke liye @AapkaUsername par message karein.")

# Bot ko chalu rakhne ke liye
print("Sanu AI is running...")
bot.infinity_polling()
