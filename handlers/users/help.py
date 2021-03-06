from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.default.generate import default_keyboard
from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: Message):
    await message.answer(
        '💭 Скачиваю весь контент из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n\t🎞: <code>instagram.com/p/*****/</code>\n\t📹: <code>instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>drtagram</code>\n\n💬 Чтобы отправить публикацию другу в диалог, воспользуйся <pre>inline</pre>-режимом бота.\n\n\t🎞: <code>@InstagramMediaDownloadBot instagram.com/p/*****/</code>\n\t📹: <code>@InstagramMediaDownloadBot instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>@InstagramMediaDownloadBot drtagram</code>', reply_markup=default_keyboard)


@dp.message_handler(text='🚨 Помощь', state='*')
async def bot_help(message: Message):
    await message.answer(
        '💭 Скачиваю весь контент из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n\t🎞: <code>instagram.com/p/*****/</code>\n\t📹: <code>instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>drtagram</code>\n\n💬 Чтобы отправить публикацию другу в диалог, воспользуйся <pre>inline</pre>-режимом бота.\n\n\t🎞: <code>@InstagramMediaDownloadBot instagram.com/p/*****/</code>\n\t📹: <code>@InstagramMediaDownloadBot instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>@InstagramMediaDownloadBot drtagram</code>', reply_markup=default_keyboard)
