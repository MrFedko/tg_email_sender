import asyncio
import os
import json
from datetime import datetime
from aiogram import types, F as f, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from magic_filter import F as MF
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.states import super_panel
from keyboards.kbrds import start_super_keyboard, crud_keyboard, products_keyboard, \
    products_read_update_keyboard
from handlers.lists import list_start_menu
from loader import bot, dp, parser, sender
from data.config import settings
from data.lexicon import lexicon
from loader import dataBase

router = Router()


# main crud menu
@router.callback_query(f.data == "db_api")
async def crud_menu(call: types.CallbackQuery, state: FSMContext):
    markup = await crud_keyboard()
    await call.message.edit_text(
        "работа с базой данных", reply_markup=markup
    )
    await call.answer()
    await state.set_state(super_panel.crud_main)


# crud products menu
@router.callback_query(f.data == "products")
async def products_menu(call: types.CallbackQuery, state: FSMContext):
    markup = await products_keyboard()
    await  call.message.edit_text(
        "практики", reply_markup=markup
    )
    await call.answer()
    await state.set_state(super_panel.crud_products)


# create product
@router.callback_query(f.data == "create_product")
async def products_create(call: types.CallbackQuery, state: FSMContext):
    btn_cancel = InlineKeyboardBuilder()
    btn_cancel.button(text=lexicon["button_back"], callback_data="products")
    await call.message.edit_text(
        """Создать практику.
Первой строкой напиши название практики как в тильде (заглавные если есть).
Вторая строка - тема письма.
Дальше тело письма.
Там где должно быть имя клиента, вставь {name}""", reply_markup=btn_cancel.as_markup()
    )
    await call.answer()
    await state.set_state(super_panel.product_create)


# get text for new product
@router.message(StateFilter(super_panel.product_create), flags={"chat_action": "typing"})
async def prod_create(message: types.Message, state: FSMContext):
    text = message.text.replace('"', '').replace("'", '').replace("“", '').replace("”", '').replace("/", "")
    lines = text.split('\n', 2)
    name = lines[0]
    theme = lines[1] if len(lines) > 1 else ''
    remaining_text = lines[2] if len(lines) > 2 else ''
    dataBase.new_product(name, theme, remaining_text)
    await message.answer(f"Практика {name} добавлена")
    markup = await start_super_keyboard()
    await list_start_menu(message, reply_markup=markup)
    await state.clear()


# read products
@router.callback_query(f.data == "read_product")
async def prods_read(call: types.CallbackQuery, state: FSMContext):
    markup = await products_read_update_keyboard("read")
    await call.message.edit_text(
        "Все практики", reply_markup=markup
    )
    await call.answer()
    await state.set_state(super_panel.products_read)


# read product
@router.callback_query(lambda f: f.data.startswith('readkey'))
async def prod_read(call: types.CallbackQuery, state: FSMContext):
    markup = await products_read_update_keyboard("read")
    result = dataBase.read_product(call.data.split()[1])
    text = ""
    for line in result:
        text += line + "\n"
    await call.message.edit_text(text, reply_markup=markup)
    await call.answer()
    await state.clear()


# update products
@router.callback_query(f.data == "update_product")
async def prods_update(call: types.CallbackQuery, state: FSMContext):
    markup = await products_read_update_keyboard("update")
    await call.message.edit_text(
        "Все практики", reply_markup=markup
    )
    await call.answer()
    await state.set_state(super_panel.products_update)


# update product
@router.callback_query(lambda f: f.data.startswith('updatekey'))
async def prod_update(call: types.CallbackQuery, state: FSMContext):
    btn_cancel = InlineKeyboardBuilder()
    btn_cancel.button(text=lexicon["button_back"], callback_data="update_product")
    await call.message.edit_text(
        f"""Редактировать практику.
Первой строкой укажи номер практики. Это {call.data.split()[1]}
Второй строкой напиши название практики как в тильде (заглавные если есть).
Третья строка - тема письма.
Дальше тело письма.
Там где должно быть имя клиента, вставь {{name}}""", reply_markup=btn_cancel.as_markup()
    )
    await call.answer()
    await state.set_state(super_panel.product_update)


# get text for update product
@router.message(StateFilter(super_panel.product_update), flags={"chat_action": "typing"})
async def prod_update_get_text(message: types.Message, state: FSMContext):
    text = message.text.replace('"', '').replace("'", '').replace("“", '').replace("”", '')
    lines = text.split('\n', 3)
    prod_id = lines[0]
    name = lines[1]
    theme = lines[2] if len(lines) > 2 else ''
    remaining_text = lines[3] if len(lines) > 3 else ''
    dataBase.update_product(prod_id, name, theme, remaining_text)
    await message.answer(f"Практика {name} изменена")
    markup = await start_super_keyboard()
    await list_start_menu(message, reply_markup=markup)
    await state.clear()
