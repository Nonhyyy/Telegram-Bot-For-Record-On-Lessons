from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_panel_kb():

    kb = InlineKeyboardBuilder()

    kb.button(text="📚 Все записи", callback_data="admin_records")
    kb.button(text="➕ Добавить предмет", callback_data="add_lesson")
    kb.button(text="❌ Удалить предмет", callback_data="delete_lesson")

    kb.adjust(1,2)

    return kb.as_markup()