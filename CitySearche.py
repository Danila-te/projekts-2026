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
def display_city_information(city_info):
    info = ""
    if city_info:
        if 'results' in city_info:
            info += "City Information:"
            for city_data in city_info['results']:
                info += f"Name: {city_data['name']}"
                info += f"Country: {city_data['country']}"
                info += f"Country code: {city_data['country_code']}"
                if 'population' in city_data and city_data['population'] > 0:
                    info += f"Population: {city_data['population']}"
                else:
                    info += f"Population: nav"
                info +=f"Timezone: {city_data['timezone']}"
                info +=f"Latitude: {city_data['latitude']}"
                info +=f"Longitude: {city_data['longitude']}"
                info +="-----------------------"
        else:
            info += "City nav."
    else:
        info += "No city information available."
    return 

# izveido bota pieslēgumu Telegram
app = ApplicationBuilder().token("8656940100:AAHQwa_l33QJtwlxViDZWqd6GlmeC3C6W8U").build()

# komanda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, i'am a CitySearch bot, this is all my funktion:\n""1)/search - search city by name.\n"
                                    "3)weather - sah weather in oet city\n")

    # komanda /hello
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user)
    city = get_city_information(update.message.text)
    city_info = display_city_information(city)
    await update.message.reply_text(city_info)

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
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("qrcod", qrcod))
app.run_polling(allowed_updates=Update.ALL_TYPES)