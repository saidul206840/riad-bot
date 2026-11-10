import os
import telebot
import google.generativeai as genai
from PIL import Image
import io

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ Riad Bot 24h Live! Chart er photo pathao.")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    try:
        bot.reply_to(m, "⏳ Chart analysis korchi...")
        file_info = bot.get_file(m.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image = Image.open(io.BytesIO(downloaded_file))
        
        prompt = "You are a trading expert. Analyze this chart image. Answer in Bangla. Format: 1. SIGNAL: BUY/SELL/WAIT 2. ENTRY price 3. STOP LOSS 4. TAKE PROFIT 1 & 2 5. Reason: 3 points 6. Confidence: %"
        
        response = model.generate_content([prompt, image])
        bot.reply_to(m, response.text)
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot is running...")
bot.infinity_polling()
