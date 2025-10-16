import telebot
import requests
from io import BytesIO
from PIL import Image
from flask import Flask

TOKEN = "8261530343:AAHMnH612XUQ4LV5mAJwYHmFb9mLHbEY0R0"
HUGGINGFACE_API = "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"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает!"

def remove_bg_hf(image_bytes):
    url = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API}"}
    response = requests.post(url, headers=headers, data=image_bytes)
    if response.status_code == 200:
        return response.content
    else:
        print("Ошибка HF:", response.text)
        return None

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "🔄 Обрабатываю фото, подожди немного...")

        # Получаем фото
        file_info = bot.get_file(message.photo[-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
        img_bytes = requests.get(file_url).content

        # Удаляем фон через Hugging Face
        result = remove_bg_hf(img_bytes)
        if not result:
            bot.reply_to(message, "❌ Ошибка при удалении фона.")
            return

        fg = Image.open(BytesIO(result)).convert("RGBA")

        # Создаём шаблон
        bg = Image.new("RGB", (1080, 1440), "#EFEFEF")

        # Масштабируем изображение
        fg = fg.resize((900, 1200))
        bg.paste(fg, (90, 120), mask=fg)

        # Отправляем результат
        bio = BytesIO()
        bio.name = 'result.jpg'
        bg.save(bio, 'JPEG')
        bio.seek(0)
        bot.send_photo(message.chat.id, bio)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

import threading
threading.Thread(target=lambda: bot.infinity_polling()).start()
