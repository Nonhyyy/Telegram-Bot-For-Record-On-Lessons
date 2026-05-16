from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton,Message)

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.admin_kb import admin_panel_kb
from db.requests import (get_all_records,admin_delete_record, add_lesson, delete_lesson, get_lessons)
from states.admin_states import AddLesson

router = Router()


@router.callback_query(F.data == "admin_panel")
async def open_admin_panel(callback: CallbackQuery):

    await callback.message.answer("⚙️ Админ панель",reply_markup=admin_panel_kb())
    await callback.answer()


@router.callback_query(F.data == "admin_records")
async def admin_records(callback: CallbackQuery,session: AsyncSession):

    records = await get_all_records(session)

    if not records:
        await callback.message.answer("Записей нет.")
        await callback.answer()
        return
    for record in records:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="❌ Удалить запись",callback_data=f"admin_delete_record_{record.id}")]])

        text = (
            f"👤 @{record.user.user_name}\n"
            f"📖 {record.lesson.name}\n"
            f"📅 {record.date.strftime('%d.%m.%Y')}\n"
            f"🕒 {record.time.strftime('%H:%M')}")
        await callback.message.answer(text,reply_markup=kb)
    await callback.answer()

@router.callback_query(
    F.data.startswith("admin_delete_record_"))
async def admin_delete_record_handler(callback: CallbackQuery,session: AsyncSession):
    record_id = int(callback.data.split("_")[-1])
    success = await admin_delete_record(session,record_id)
    if success:
        await callback.message.edit_text("✅ Запись удалена")
    else:
        await callback.message.edit_text("❌ Запись не найдена")
    await callback.answer()

@router.callback_query(F.data == "add_lesson")
async def add_lesson_start(callback: CallbackQuery,state: FSMContext):
    await state.set_state(AddLesson.waiting_for_name)

    await callback.message.answer("Введите название предмета:")
    await callback.answer()


@router.message(AddLesson.waiting_for_name)
async def add_lesson_finish(message: Message,state: FSMContext,session: AsyncSession):

    lesson_name = message.text.strip()

    success = await add_lesson(session,lesson_name)
    if success:
        await message.answer(
            f"✅ Предмет '{lesson_name}' добавлен")
    else:
        await message.answer("❌ Такой предмет уже существует")

    await state.clear()

@router.callback_query(F.data == "delete_lesson")
async def delete_lesson_menu(callback: CallbackQuery,session: AsyncSession):
    lessons = await get_lessons(session)
    if not lessons:

        await callback.message.answer("Предметов нет.")
        await callback.answer()
        return

    for lesson in lessons:

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить",callback_data=f"delete_lesson_{lesson.id}")]])

        await callback.message.answer(f"📖 {lesson.name}",reply_markup=kb)
    await callback.answer()

@router.callback_query(
    F.data.startswith("delete_lesson_"))
async def delete_lesson_handler(callback: CallbackQuery,session: AsyncSession):

    lesson_id = int(callback.data.split("_")[-1])

    success = await delete_lesson(session,lesson_id)
    if success:

        await callback.message.edit_text("✅ Предмет удалён")
    else:
        await callback.message.edit_text("⛔ Ошибка удаления")
    await callback.answer()