import re


class Parser:
    def pars_text(self, text):
        # Регулярные выражения для поиска нужных данных
        item_pattern = re.compile(r'\d+\.\s([А-ЯЁа-яё\s]+):')
        name_pattern = re.compile(r'Name:\s(.+)', re.MULTILINE)
        email_pattern = re.compile(r'Email:\s(.+)', re.MULTILINE)
        phone_pattern = re.compile(r'Phone:\s(.+)', re.MULTILINE)

        # Поиск данных в сообщении
        item_match = item_pattern.search(text)
        name_match = name_pattern.search(text)
        email_match = email_pattern.search(text)
        phone_match = phone_pattern.search(text)

        # Получение значений из найденных совпадений
        item_text = item_match.group(1) if item_match else None
        name = name_match.group(1) if name_match else None
        email = email_match.group(1) if email_match else None
        phone = phone_match.group(1) if phone_match else None
        return item_text, name, email, phone

# Order #1729724162
# 1. РЕФЛЕКС ОРГАЗМА: 10 (1 x 10) 12 июня - 14:00-17:30
# The order is paid for.
# Payment Amount: 10 RUB
# Payment ID: YooKassa: 2dde5af2-000f-5000-a000-110e651e0e7b
#
# Purchaser information:
# Name: Михаил Сергеевич Федько
# Email: miklerst@mail.ru
# Phone: +79618518825
#
# Additional information:
# Transaction ID: 9488913:6264465761
# Block ID: rec750027133
# Form Name: Cart
# https://amaalieva.com/#!/tab/744909242-2
# -----
