from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict

class SelectVariantCallback(CallbackData, prefix="SelectVariantCallback"):
    value: int
    right: int


def create_variant_keyboard(variants: Dict[int, bool]):
    builder = InlineKeyboardBuilder()

    for number, value in variants.items():
        builder.button(text=str(number), callback_data=SelectVariantCallback(value=number, right=value).pack())
        
    builder.adjust(2)  # Set width to 2 buttons per row
    return builder.as_markup()
