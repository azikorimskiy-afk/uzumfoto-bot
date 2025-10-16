import telebot
from rembg import remove
from PIL import Image
from io import BytesIO
import os

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("8261530343:AAHMnH612XUQ4LV5mAJwYHmFb9mLHbEY0R0")
bot = telebot.TeleBot(8261530343:AAHMnH612XUQ4LV5mAJwYHmFb9mLHbEY0R0)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем фото
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_image = Image.open(BytesIO(downloaded_file)).convert("RGBA")

        # Удаляем фон
        output = remove(input_image)

        # Создаем шаблон с серым фоном #EFEFEF (1080x1440)
        background = Image.new("RGBA", (1080, 1440), "#EFEFEF")

        # Масштабируем и вставляем в центр
        output.thumbnail((1000, 1300))
        bg_w, bg_h = background.size
        offset = ((bg_w - output.width) // 2, (bg_h - output.height) // 2)
        background.paste(output, offset, output)

        # Отправляем результат пользователю
        bio = BytesIO()
        bio.name = 'result.png'
        background.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(message.chat.id, bio)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

print("🚀 Бот запущен и ожидает фото...")
bot.infinity_polling()
