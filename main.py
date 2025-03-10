import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from professions import professions
from cities import cities
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
