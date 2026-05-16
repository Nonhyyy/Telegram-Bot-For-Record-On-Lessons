from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(is_admin=False):
    keyboard=[
        [InlineKeyboardButton(text="📒 Записаться",callback_data="start_booking")],
        [InlineKeyboardButton(text="📋 Мои записи",callback_data="my_records")],
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton(text="Админ-панель",callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)