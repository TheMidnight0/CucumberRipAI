import os, asyncio, re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, InputMediaPhoto
import ai

API_TOKEN = os.getenv('BOT_TOKEN') or ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.answer("Здравствуй, путник! Я – жнец огуречной судьбы, знающий о всех тонкостях работы с ними. " \
    "Все просто, отправь мне изображение огурцов, и я укажу тебе их уровень зрелости...или съедобности. " \
    "Также ты в любой момент можешь изменить параметры предсказаний, просто отправь в чат:\n" \
    "iou = 0.0-1.0 - это позволит мне убирать предсказания, которые перекрывают другие больше чем на iou %\n" \
    "conf = 0.0-1.0 - это позволит мне убирать предсказания, в которых я уверен меньше чем на conf %")

def parse_params(param_string):
    if param_string == None: 
        return None, None

    # Инициализируем параметры по умолчанию
    conf = None
    iou = None

    # Ищем значения параметров в строке
    conf_match = re.search(r'conf=([\d.]+)', param_string)
    iou_match = re.search(r'iou=([\d.]+)', param_string)

    # Если найдено значение для conf, преобразуем его в float
    if conf_match:
        conf = float(conf_match.group(1))

    # Если найдено значение для iou, преобразуем его в float
    if iou_match:
        iou = float(iou_match.group(1))

    return conf, iou

@dp.message()
async def classify(message: types.Message):
    if parse_params(message.text) != (None, None):
        conf, iou = parse_params(message.text)
        ai.conf_model(conf, iou)
        if (iou != None): 
            await message.answer("Изменен порог IOU на %f" %iou)
        if (conf != None): 
            await message.answer("Изменен порог уверенности на %f" %conf)
    elif parse_params(message.caption) != (None, None):
        conf, iou = parse_params(message.caption)
        ai.conf_model(conf, iou)
        if (iou != None): 
            await message.answer("Изменен порог IOU на %f" %iou)
        if (conf != None): 
            await message.answer("Изменен порог уверенности на %f" %conf)

    if message.photo:
        media_group = []
        for photo in message.photo[-int(len(message.photo) / 3):]:
            file = await bot.get_file(photo.file_id)
            file_bytes = await bot.download_file(str(file.file_path))

            predicted = ai.predict(file_bytes.read()) # type: ignore
            media_group.append(InputMediaPhoto(media=BufferedInputFile(predicted, filename="image.jpg")))

        await message.answer_media_group(media=media_group)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())