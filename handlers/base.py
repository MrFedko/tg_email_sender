import asyncio
import os
import json
import re
from datetime import datetime
from aiogram import types, F as f, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from magic_filter import F as MF
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.states import Super_panel
from keyboards.kbrds import start_super_keyboard, products_dates_keyboard, products_read_update_keyboard, \
    products_for_group_mail_keyboard
from handlers.lists import list_start_menu
from loader import bot, dp, parser, sender
from data.config import settings
from data.lexicon import lexicon
from loader import dataBase

router = Router()


# старт
@router.message(Command("start"), flags={"chat_action": "typing"})
async def start(message: types.Message):
    markup = await start_super_keyboard()
    if str(message.from_user.id) in settings.admins:
        await list_start_menu(message, reply_markup=markup)


# создание бд
@router.message(Command("createdb"), flags={"chat_action": "typing"})
async def createdb(message: types.Message):
    dataBase.create_tables()
    await message.answer("DB is ready")


# кнопка рассылки
@router.callback_query(f.data == "mail")
async def send_mail(call: types.CallbackQuery, state: FSMContext):
    btn_cancel = InlineKeyboardBuilder()
    btn_cancel.button(text=lexicon["button_back"], callback_data="cancel_mail")
    await call.message.edit_text(
        "отправь сюда заявку", reply_markup=btn_cancel.as_markup()
    )
    await call.answer()
    await state.set_state(Super_panel.mail)


# отправка соло письма
@router.message(StateFilter(Super_panel.mail), flags={"chat_action": "typing"})
async def send_email(message: types.Message, state: FSMContext):
    text = message.text.replace('"', '').replace("'", '').replace("“", '').replace("”", '').replace("/", "")
    products, name, mail, phone = parser.pars_text(text)
    user_id = dataBase.read_client_id(mail)
    for product in products:
        mail_theme, mail_text = dataBase.get_text(product[0])
        mail_text = mail_text.format(name=name)
        sender.send_mail(mail, mail_theme, mail_text)
        dataBase.new_order(user_id[0], product[0], product[1])
    markup = await start_super_keyboard()
    client = dataBase.read_client(mail)
    if not client:
        dataBase.new_client(name, mail, phone)
    await message.answer(f"""{products}, {name}, {mail}, {phone}
Письмо отправлено.""", reply_markup=markup)
    await state.clear()


#  кнопка назад
@router.callback_query(f.data == "cancel_mail")
async def back(call: types.CallbackQuery, state: FSMContext):
    markup = await start_super_keyboard()
    await call.message.edit_text("Start screen", reply_markup=markup)
    await state.clear()


# выбор даты для массовой рассылки
@router.callback_query(f.data == "group_mail")
async def choice_group_mail(call: types.CallbackQuery, state: FSMContext):
    markup = await products_dates_keyboard()
    await call.message.edit_text(
        "выбери день мероприятия", reply_markup=markup
    )
    await call.answer()
    await state.set_state(Super_panel.group_mail)

@router.callback_query(lambda f: f.data.startswith('proddates'))
async def send_group_mail(call: types.CallbackQuery, state: FSMContext):
    markup = await products_for_group_mail_keyboard(call.data.split(" ", 1)[1])
    await call.message.edit_text("""Сделать массовую рассылку.
Выбери письмо, которое необходимо разослать.""", reply_markup=markup
    )
    await call.answer()
    await state.set_state(Super_panel.send_group_mail)

@router.callback_query(f.data == "groupsend")
async def now_send_group_mail(call: types.CallbackQuery, state: FSMContext):
    markup = await start_super_keyboard()
    _, date, product = call.data.split("/")
    users = dataBase.read_client_id_by_product_day(date)
    text = ""
    for user_mail, user_name in users:
        mail_theme, mail_text = dataBase.get_text(product)
        mail_text = mail_text.format(name=user_name)
        sender.send_mail(user_mail, mail_theme, mail_text)
        text += f"{user_name}: {user_mail} \n"
    await call.answer(f"""Письма отправлены для:
{text}""", reply_markup=markup)
    await state.clear()
