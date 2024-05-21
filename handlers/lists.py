from aiogram.types import CallbackQuery, Message
from typing import Union
from keyboards.kbrds import start_super_keyboard
from data.lexicon import lexicon


async def list_start_menu(message: Union[CallbackQuery, Message], **kwargs):
    text = lexicon["/start"].format(name=message.from_user.first_name)

    if isinstance(message, Message):
        await message.answer(text, reply_markup=kwargs["reply_markup"])

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text, reply_markup=kwargs["reply_markup"])
