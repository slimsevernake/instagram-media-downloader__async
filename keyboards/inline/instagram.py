from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import stories_callback


def user_keyboard(username: str, is_private: bool, posts_button: bool = True):
    keyboard = InlineKeyboardMarkup(row_width=2)
    instagram_link = InlineKeyboardButton(text='📸 Instagram', url=f'https://www.instagram.com/{username}')
    if not is_private:
        stories_button = InlineKeyboardButton(text='📹 Истории', callback_data=stories_callback.new(username=username))
        if posts_button:
            posts_button = InlineKeyboardButton(text='📽 Посты', switch_inline_query_current_chat='')
            keyboard.add(stories_button, posts_button, instagram_link)
        else:
            keyboard.add(stories_button, instagram_link)
    else:
        keyboard.add(instagram_link)
    return keyboard


def media_keyboard(link: str):
    keyboard = InlineKeyboardMarkup()
    media_button = InlineKeyboardButton(text='📎', url=link)
    keyboard.add(media_button)
    return keyboard
