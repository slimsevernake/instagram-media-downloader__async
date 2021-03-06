from aiogram.types import Message
from data.config import BOT_NAME
from keyboards.default.generate import default_keyboard
from loader import dp


@dp.message_handler(commands=['referral'], state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=f'🤖 Пригласи друга по своей реферальной ссылке и получи от 3 до 7 дней бесплатной подписки\n<code>t.me/{BOT_NAME}?start={message.chat.id}</code>', reply_markup=default_keyboard)


@dp.message_handler(text='👥 Реферальная программа', state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=f'🤖 Пригласи друга по своей реферальной ссылке и получи от 3 до 7 дней бесплатной подписки\n<code>t.me/{BOT_NAME}?start={message.chat.id}</code>', reply_markup=default_keyboard)
