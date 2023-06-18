import logging
import openai
import requests
import telebot

# Configura el token de tu bot proporcionado por BotFather
TOKEN = '6032931983:AAHWoC6PjFbKTb9zG7azzZiV057gtB7wV68'

# Configura tu clave de API de OpenAI
OPENAI_API_KEY = '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'

# Configura el modelo y el motor de OpenAI
OPENAI_MODEL = 'gpt-3.5-turbo'

# Configuración de registro (opcional)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Configura el cliente de OpenAI
openai.api_key = OPENAI_API_KEY

# Historial de conversación
conversation_history = []

# Crea una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Función para obtener el pronóstico del clima utilizando la API OpenWeatherMap
def get_weather_forecast(city):
    API_KEY = '6ad8eae6a6d1eaf3409ddcd2558a85d0'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if 'weather' in data and 'main' in data['weather'][0]:
        weather_description = data['weather'][0]['main']
    else:
        weather_description = 'No se pudo obtener el pronóstico del clima.'

    if 'main' in data and 'temp' in data['main']:
        temperature = data['main']['temp']
    else:
        temperature = 'No se pudo obtener la temperatura.'

    return f"El pronóstico del clima en {city} es {weather_description} con una temperatura de {temperature}°C."

# Función para generar una respuesta utilizando la API de OpenAI
def generate_response(message):
    global conversation_history

    if message.lower().startswith('clima'):
        city = message[6:].strip()
        weather_forecast = get_weather_forecast(city)
        response_text = weather_forecast
    else:
        # Agregar el mensaje del usuario al historial de conversación
        conversation_history.append({"role": "user", "content": message})

        # Generar una respuesta utilizando el historial de conversación
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *conversation_history
            ]
        )

        # Agregar la respuesta al historial de conversación
        generated_text = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": generated_text})

        signature = "\n\nPowered By @KyleProyectOficial"
        response_text = generated_text + signature

    return response_text

# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "¡Hola! El bot ha sido encendido.")

# Manejador para los mensajes de texto
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id
    
    response_text = generate_response(text)
    
    bot.send_message(chat_id=chat_id, text=response_text)

# Inicia el bot
def run_bot():
    bot.polling()

# Ejecuta el bot
if __name__ == '__main__':
    run_bot()
