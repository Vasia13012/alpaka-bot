from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import CommandStart
import logging
import os
from fastapi import FastAPI
from aiogram.types import Update
from aiogram.dispatcher.webhook import get_webhook_handler
import uvicorn

# === Налаштування логування та токена ===
API_TOKEN = os.getenv("API_TOKEN")
logging.basicConfig(level=logging.INFO)

# === Ініціалізація бота ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# === Reply клавіатура (під полем вводу) ===
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.row(
    KeyboardButton("Як нас знайти?"),
    KeyboardButton("Контакти")
)
reply_keyboard.row(
    KeyboardButton("Донат (Coming soon)"),
    KeyboardButton("?")
)

# === Inline клавіатура (під вітальним повідомленням) ===
welcome_keyboard = InlineKeyboardMarkup(row_width=1)
welcome_keyboard.add(
    InlineKeyboardButton("📍 Навігація", url="https://t.me/MyAlpaka")
)
welcome_keyboard.row(
    InlineKeyboardButton("🌐 Соцмережі", url="https://t.me/MyAlpaka/6/10"),
    InlineKeyboardButton("📰 Новини", url="https://t.me/MyAlpaka/8")
)

# === Обробка команди /start ===
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    username = message.from_user.username or "друже"
    welcome_text = (
        f"👋 Вітаємо тебе @{username}\n"
        f"Це \"Alpaka\" — молодь, яка дихає глибиною й сміхом.\n"
        f"Це люди, які шукають сенсу, світла й тепла.\n"
        f"🌿 Ми молимось, любимо активний відпочинок,\n"
        f"говоримо щиро, сміємось до ночі й тримаємось разом.\n"
        f"Можливо, ти тут випадково. Але точно не даремно.\n"
        f"Добре, що ти з нами 💛."
    )
    await message.answer(welcome_text, reply_markup=welcome_keyboard)
    await message.answer("Обери опцію нижче ⬇️", reply_markup=reply_keyboard)

# === FastAPI додаток ===
app = FastAPI()

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://alpaka-bot-production.up.railway.app{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.process_update(telegram_update)

if __name__ == "__main__":
    uvicorn.run("bot_railway_main:app", host="0.0.0.0", port=10000)
