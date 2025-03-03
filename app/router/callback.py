from aiogram import Router
from aiogram.types import CallbackQuery

from keyboard_ import SelectVariantCallback, create_variant_keyboard
from database import PostgresDB
from .utils import generate_question

router = Router()

@router.callback_query(SelectVariantCallback.filter())
async def select_variant(callback: CallbackQuery, db: PostgresDB):
    callback_data = callback.data
    variant = SelectVariantCallback.unpack(callback_data)
    
    await callback.answer("Правильно" if variant.value == variant.right else f"Неправильно. Правильный ответ: {variant.right}")
    string, variants = generate_question()    
    return await callback.message.edit_text(string, reply_markup=create_variant_keyboard(variants))