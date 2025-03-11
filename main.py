import json
import time
import requests
import random
import nest_asyncio
from natasha import MorphVocab
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from professions import professions
from cities import cities

# Регистрируем nested event loop
nest_asyncio.apply()

# Инициализация морфологического анализатора
morph = MorphVocab()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Привет! Я генератор профессий будущего.\n"
        "Напиши своё имя и получи предсказание!"
    )

async def generate_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.message.text
    profession = random.choice(professions)
    city = random.choice(cities)

    # Формируем текстовое предсказание
    response = (
        f"{name}, через 10 лет ты будешь:\n"
        f"🔥 *{profession}* 🔥\n"
        f"🌎 В *{city}*!\n\n"
        "Это предсказание сгенерировано нейросетью 🤖"
    )
    await update.message.reply_text(response, parse_mode="Markdown")


# Класс для работы с Fusion Brain API
class Text2ImageAPI:
    def init(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


# Инициализация API
fusion_brain_api = Text2ImageAPI(
    url='https://api-key.fusionbrain.ai/',
    api_key='1F9C14583FF95C530D2321E1C60A2200',
    secret_key='D68F219B46DCAFBF1E49E24094142B12'
)
