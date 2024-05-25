from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.lexicon import lexicon
from loader import dataBase


async def start_super_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=lexicon["send_mail"], callback_data="mail"),
        InlineKeyboardButton(text=lexicon["db_button"], callback_data="db_api"),
        InlineKeyboardButton(text=lexicon["group_mail"], callback_data="group_mail"),
    ]
    return markup.row(*buttons, width=2).as_markup()


async def crud_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=lexicon["products"], callback_data="products"),
        InlineKeyboardButton(text=lexicon["clients"], callback_data="clients"),
        InlineKeyboardButton(text=lexicon["button_back"], callback_data="cancel_mail"),
    ]
    return markup.row(*buttons, width=2).as_markup()


async def products_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=lexicon["create"], callback_data="create_product"),
        InlineKeyboardButton(text=lexicon["read"], callback_data="read_product"),
        InlineKeyboardButton(text=lexicon["update"], callback_data="update_product"),
        InlineKeyboardButton(text=lexicon["button_back"], callback_data="db_api"),
    ]
    return markup.row(*buttons, width=2).as_markup()


async def products_read_update_keyboard(task) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = []
    all_products = dataBase.read_products()
    for product in all_products:
        buttons.append(InlineKeyboardButton(text=product[1], callback_data=f"{task}key {product[0]}"))
    buttons.append(InlineKeyboardButton(text=lexicon["button_back"], callback_data="products"))
    return markup.row(*buttons, width=2).as_markup()


async def products_for_group_mail_keyboard(date) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = []
    all_products = dataBase.read_products()
    for product in all_products:
        buttons.append(InlineKeyboardButton(text=product[1], callback_data=f"groupsend /{date}/{product[0]}"))
    buttons.append(InlineKeyboardButton(text=lexicon["button_back"], callback_data="group_mail"))
    return markup.row(*buttons, width=2).as_markup()



async def products_dates_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = []
    all_dates = dataBase.read_dates()
    for date in all_dates:
        buttons.append(InlineKeyboardButton(text=date, callback_data=f"proddates {date}"))
    buttons.append(InlineKeyboardButton(text=lexicon["button_back"], callback_data="cancel_mail"))
    return markup.row(*buttons, width=2).as_markup()
