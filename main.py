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


