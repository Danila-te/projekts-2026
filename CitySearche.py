import urllib.request
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def get_city_information(city):
    link = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=3&language=en&format=json"

    with urllib.request.urlopen(link) as response:
        data = response.read().decode('utf-8')

    return json.loads(data)
def display_city_information(city_info):
    info = ""
    if city_info:
        if 'results' in city_info:
            info += "City Information:\n"
            for city_data in city_info['results']:
                info += f"Name: {city_data['name']}\n"
                info += f"Country: {city_data['country']}\n"
                info += f"Country code: {city_data['country_code']}\n"
                if 'population' in city_data and city_data['population'] > 0:
                    info += f"Population: {city_data['population']}\n"
                else:
                    info += f"Population: nav\n"
                info +=f"Timezone: {city_data['timezone']}\n"
                info +=f"Latitude: {city_data['latitude']}\n"
                info +=f"Longitude: {city_data['longitude']}\n"
                info +="-----------------------\n"
        else:
            info += "City nav.\n"
    else:
        info += "No city information available.\n"
    return info

app = ApplicationBuilder().token("8656940100:AAHQwa_l33QJtwlxViDZWqd6GlmeC3C6W8U").build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sveiki, esmu CitySearch bot, tās ir visas manas funkcijas:\n"
                                    "1)/start - atver dialoglodziņu\n"
                                    "2)/search - meklē pilsētas pēc burtiem vai burtu kombinācijām.\n"
                                    "3)/echo - pārbaudes, ko es varu dzirdēt\n")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user)
    city = get_city_information(update.message.text[8:])
    print(city)
    city_info = display_city_information(city)
    await update.message.reply_text(city_info)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I hear: " + update.message.text)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("echo", echo))
app.run_polling(allowed_updates=Update.ALL_TYPES)