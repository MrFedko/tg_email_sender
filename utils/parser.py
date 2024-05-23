import re


class Parser:
    def pars_text(self, text):
        # Регулярное выражение для поиска позиций
        item_pattern = re.compile(r'\d+\.\s([^:]+):\s\d+\s\(1\sx\s\d+\)\s(\d{1,2}\s[а-яА-Я]+)')

        # Найти все совпадения
        matches = item_pattern.findall(text)
        result = []
        # Вывод результатов
        for match in matches:
            practice, date = match
            result.append((practice.strip(), date.strip()))
        # Регулярные выражения для поиска нужных данных
        name_pattern = re.compile(r'Name:\s(.+)', re.MULTILINE)
        email_pattern = re.compile(r'Email:\s(.+)', re.MULTILINE)
        phone_pattern = re.compile(r'Phone:\s(.+)', re.MULTILINE)

        # Поиск данных в сообщении
        name_match = name_pattern.search(text)
        email_match = email_pattern.search(text)
        phone_match = phone_pattern.search(text)

        # Получение значений из найденных совпадений
        name = name_match.group(1) if name_match else None
        email = email_match.group(1) if email_match else None
        phone = phone_match.group(1) if phone_match else None
        return result, name, email, phone

# Order #1715858959
# 1. BREATHWORK "ОПОРЫ И РЕСУРСЫ": 20 (1 x 20) 23 июня - 13:30-16:30
# 2. BREATHWORK "ПУТЬ К СЕБЕ": 20 (1 x 20) 1 июня - 15:00-18:00
# The order is paid for.
# Payment Amount: 40 RUB
# Payment ID: YooKassa: 2de12b56-000f-5000-a000-1576a3dde1be
#
# Purchaser information:
# Name: Михаил Сергеевич Федько
# Email: miklerst@mail.ru
# Phone: +79618518825
#
# Additional information:
# Transaction ID: 9488913:6274716781
# Block ID: rec750027133
# Form Name: Cart
# https://amaalieva.com/#!/tab/744909242-1
# -----
