import os, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from ai import predict

API_TOKEN = os.getenv('BOT_TOKEN') or ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.answer("Здравствуй, путник! Я – жнец огуречной судьбы, знающий о всех тонкостях работы с ними. Все просто, отправь мне изображение огурцов, и я укажу тебе их уровень зрелости...или съедобности.")

@dp.message()
async def classify(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(str(file.file_path))

        predicted = predict(file_bytes.read()) # type: ignore
        input_file = BufferedInputFile(predicted, filename="image.jpg")
        await message.answer_photo(input_file)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())