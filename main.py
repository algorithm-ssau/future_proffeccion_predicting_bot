import logging
import os
import json
import base64
from io import BytesIO
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from professions_dict import professions  # Импортируем словарь профессий
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния разговора
NAME, GENDER, IT_INTEREST, MUSIC, DRINK, HOBBIES = range(6)

# Обновленные варианты ответов
GENDER_KEYBOARD = [["Парень", "Девушка"]]
IT_KEYBOARD = [["Роботы", "Биотех"], ["ИИ", "Бэкенд"], ["Фронтенд", "Аналитика"]]
MUSIC_KEYBOARD = [["Я меломан", "Рок"], ["Хип-хоп", "Ничего из этого"], ["Классика", "Джаз"]]
DRINK_KEYBOARD = [["Кофе", "Чай"], ["Ни то, ни другое"]]
HOBBIES_KEYBOARD = [["Спорт", "Кино"], ["Игры", "Книги"], ["Программирование", "Скроллить ленту"]]

# Путь к папке с изображениями
PROFESSIONS_IMAGES_DIR = "profession_images_sequential"
user_data = {}

# Mapping комбинаций ответов на ключи профессий
PROFESSION_MAPPING = professions


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.message.from_user.id] = {"name": update.message.text}
    await update.message.reply_text(
        f"Приятно познакомиться, {update.message.text}!\n\nКто ты?",
        reply_markup=ReplyKeyboardMarkup(GENDER_KEYBOARD, one_time_keyboard=True)
    )
    return GENDER


async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.message.from_user.id]["gender"] = update.message.text
    await update.message.reply_text(
        "Что тебе интересно в IT?",
        reply_markup=ReplyKeyboardMarkup(IT_KEYBOARD, one_time_keyboard=True)
    )
    return IT_INTEREST


async def handle_it(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.message.from_user.id]["it_interest"] = update.message.text
    await update.message.reply_text(
        "Какую музыку любишь?",
        reply_markup=ReplyKeyboardMarkup(MUSIC_KEYBOARD, one_time_keyboard=True)
    )
    return MUSIC


async def handle_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.message.from_user.id]["music"] = update.message.text
    await update.message.reply_text(
        "Кофе или чай?",
        reply_markup=ReplyKeyboardMarkup(DRINK_KEYBOARD, one_time_keyboard=True)
    )
    return DRINK


async def handle_drink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.message.from_user.id]["drink"] = update.message.text
    await update.message.reply_text(
        "Чем занимаешься в свободное время?",
        reply_markup=ReplyKeyboardMarkup(HOBBIES_KEYBOARD, one_time_keyboard=True)
    )
    return HOBBIES


async def get_profession_image(profession_name: str, gender: str):
    """Получаем изображение профессии в формате base64"""
    try:
        # Формируем путь к файлу
        image_path = os.path.join(PROFESSIONS_IMAGES_DIR, profession_name, f"{gender}.json")
        logger.info(f"{image_path}")

        if not os.path.exists(image_path):
            return None

        with open(image_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
            return base64.b64decode(image_data["image_base64"])
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        return None


async def handle_hobbies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers = user_data[update.message.from_user.id]
    answers["hobbies"] = update.message.text

    # Формируем ключ для поиска профессии (кортеж из ответов)
    profile_key = (
        answers.get('gender', ''),
        answers.get('it_interest', ''),
        answers.get('music', ''),
        answers.get('drink', ''),
        answers.get('hobbies', '')
    )
    # Для отладки выведем полученный ключ
    logger.info(f"Поиск профессии для ключа: {profile_key}")

    # Ищем профессию в нашем mapping-словаре
    profession_base_name = PROFESSION_MAPPING.get(profile_key)

    if not profession_base_name:
        await update.message.reply_text("Извините, не смогли определить подходящую профессию для ваших ответов")
        return ConversationHandler.END

    # Формируем полный ключ для словаря профессий
    gender_suffix = "male" if answers.get('gender') == "Парень" else "female"
    profession_key = f"{profession_base_name}"

    messages = [
        "Нейросеть раскладывает карты таро 🃏",
        "Языковые модели смотрят в будущее 👀",
        "Алгоритм проверяет предсказания всех ясновидящих 🔮",
        "Изучаем справочник перспективных профессий 📚",
        "Нейросеть гадает на кофейное гуще ☕️",
        "Нейросеть анализирует звездные карты 🌌"
    ]

    # Отправляем первое сообщение
    message = await update.message.reply_text(messages[0])

    # Меняем сообщение каждые 0.7 секунды для более динамичной анимации
    for msg in messages[1:]:
        await asyncio.sleep(1)
        await message.edit_text(msg)

    # Добавляем финальное сообщение перед результатом
    await asyncio.sleep(0.7)
    await message.edit_text("🔮 Ваше предсказание от ИИ готово!")
    await asyncio.sleep(1)

    # Формируем сообщение
    message_text = (
        f"👤 {answers['name']}\n"
        f"🚀 искуственный интеллект считает, что через 10 лет ты будешь {profession_base_name}\n"

    )

    # Пытаемся отправить изображение
    try:
        image_bytes = await get_profession_image(profession_key, gender_suffix)
        if image_bytes:
            await update.message.reply_photo(
                photo=BytesIO(image_bytes),
                caption=message_text
            )
        else:
            await update.message.reply_text(
                f"{message_text}\n\nКартинка еще не сгенерирована"
            )
    except Exception as e:
        logger.error(f"Error sending image: {e}")
        await update.message.reply_text(message_text)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Опрос отменен", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token("").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            GENDER: [MessageHandler(filters.Regex('^(Парень|Девушка)$'), handle_gender)],
            IT_INTEREST: [MessageHandler(filters.Regex('^(Роботы|Биотех|ИИ|Бэкенд|Фронтенд|Аналитика)$'), handle_it)],
            MUSIC: [
                MessageHandler(filters.Regex('^(Я меломан|Рок|Хип-хоп|Ничего из этого|Классика|Джаз)$'), handle_music)],
            DRINK: [MessageHandler(filters.Regex('^(Кофе|Чай|Ни то, ни другое)$'), handle_drink)],
            HOBBIES: [MessageHandler(filters.Regex('^(Спорт|Кино|Игры|Книги|Программирование|Скроллить ленту)$'),
                                     handle_hobbies)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
