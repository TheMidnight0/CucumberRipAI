import os, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = os.getenv('BOT_TOKEN') or ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.answer("Здравствуй, путник! Я – жнец огуречной судьбы, знающий о всех тонкостях работы с ними. Отправь мне изображение огурцов, и я укажу тебе их уровень зрелости, только осторожно – я не люблю гнилые. Готов отправить первый огурец?")

@dp.message()
async def classify(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        await message.answer_photo(photo.file_id)
        await message.answer("Ответ")

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())