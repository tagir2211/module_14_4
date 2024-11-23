from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt_info = KeyboardButton('Информация')
bt_calc = KeyboardButton('Расчет')
bt_buy = KeyboardButton('Купить')
kb.add(bt_info, bt_calc, bt_buy)

inl_kb = InlineKeyboardMarkup(resize_keyboard=True)
inl_bt_cal = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inl_bt_for = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
inl_kb.add(inl_bt_cal, inl_bt_for)

inl_kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
inl_kb_pr_1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying1')
inl_kb_pr_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying2')
inl_kb_pr_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying3')
inl_kb_pr_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying4')

inl_kb_buy.add(inl_kb_pr_1, inl_kb_pr_2, inl_kb_pr_3, inl_kb_pr_4)
