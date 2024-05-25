from aiogram.filters.state import State, StatesGroup


class Super_panel(StatesGroup):
    mail = State()
    crud_main = State()
    crud_products = State()
    product_create = State()
    products_read = State()
    products_update = State()
    product_update = State()
    group_mail = State()
    send_group_mail = State()
