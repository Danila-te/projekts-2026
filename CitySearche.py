import urllib.request
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import qrcode
def get_city_information(city):
    link = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=3&language=en&format=json"

    with urllib.request.urlopen(link) as response:
        data = response.read().decode('utf-8')

    return json.loads(data)

# izveido bota pieslēgumu Telegram
app = ApplicationBuilder().token("8656940100:AAHQwa_l33QJtwlxViDZWqd6GlmeC3C6W8U").build()

# komanda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, i'am a CitySearch bot, this is all my funktion:\n""1)/search - search city by name.\n"
                                    "3)weather - sah weather in oet city\n")

    # komanda /hello
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user)
    await update.message.reply_text(f'Hello {update.effective_user.first_name} {update.effective_user.last_name}')

    # komanda /echo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I hear: " + update.message.text)

async def qrcod(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Building QR code: " + update.message.text[8:])
    img = qrcode.make(update.message.text[8:])
    img.save('qr.png', scale=7)
    await update.message.reply_photo('qr.png')

# savieno čata komandu ar funkciju
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("qrcod", qrcod))
app.run_polling(allowed_updates=Update.ALL_TYPES)