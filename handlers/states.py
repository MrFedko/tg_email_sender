from aiogram.filters.state import State, StatesGroup


class super_panel(StatesGroup):
    mail = State()
    crud_main = State()
    crud_products = State()
    product_create = State()
    products_read = State()
    products_update = State()
    product_update = State()
