import telebot
from flask import Flask, request
from rembg import remove
from PIL import Image
import io

TOKEN = "8261530343:AAHMnH612XUQ4LV5mAJwYHmFb9mLHbEY0R0"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 📸 Обработка изображений
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        input_img = Image.open(io.BytesIO(downloaded))
        output = remove(input_img)
        output = output.convert("RGBA")
        background = Image.new("RGBA", (1080, 1440), "#EFEFEF")
        output.thumbnail((1080, 1440))
        background.paste(output, ((1080 - output.width)//2, (1440 - output.height)//2), output)

        bio = io.BytesIO()
        background.save(bio, "PNG")
        bio.seek(0)
        bot.send_photo(message.chat.id, bio)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка обработки: {e}")

# 🌐 Webhook endpoints
@app.route(f"/{TOKEN}", methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{render_app_name}.onrender.com/{TOKEN}")
    return "Webhook установлен!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
