from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import text
from crud_functions import *
from kb import *


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


API = '_'
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())
TABLE_NAME = 'Product'
initiate_db(TABLE_NAME)
add_data(TABLE_NAME)
data = {}


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        await message.answer(get_all_products(TABLE_NAME, i + 1))
        with open(f'{i}.jpeg', 'rb') as photo:
            await message.answer_photo(photo)
    await message.answer('Выберите продукт для покупки:', reply_markup=inl_kb_buy)


@dp.callback_query_handler(text='product_buying1')
async def get_product1(call):
    await call.message.answer(f'Вы выбрали {text.name[0]}')
    await call.answer()


@dp.callback_query_handler(text='product_buying2')
async def get_product2(call):
    await call.message.answer(f'Вы выбрали {text.name[1]}')
    await call.answer()


@dp.callback_query_handler(text='product_buying3')
async def get_product3(call):
    await call.message.answer(f'Вы выбрали {text.name[2]}')
    await call.answer()


@dp.callback_query_handler(text='product_buying4')
async def get_product4(call):
    await call.message.answer(f'Вы выбрали {text.name[3]}')
    await call.answer()


@dp.message_handler(text='Расчет')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=inl_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6,25 x рост(см) - 5 x возраст(лет) + 5')
    await call.answer()


# функция для проверки ответа, млжет ли быть ответ чилом

def try_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


# реагируем на текст 'Calories' и запрашиваем возраст

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


# проверяем возраст, если возрас передан коректно то запускаем функцию set_growth, если нет то запрашиваем возраст еще раз

@dp.message_handler(state=UserState.age)
async def chec_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    if try_int(data['age']):
        await set_growth(message, state, data=data)
    else:
        await message.answer('Возраст введен не корректно, попробуйте еще раз.')

        await set_age(message)


# если в data на была записана информация о возрасте записываем ее и запрашиваем рост, если информация уже есть просто запрашиваем рост

@dp.message_handler(state=UserState.age)
async def set_growth(message, state, data):
    if 'age' in data.keys():
        await message.answer('Введите свой рост')
        await UserState.growth.set()
    else:
        await state.update_data(age=message.text)
        data = await state.get_data()
        await message.answer('Введите свой рост')
        await UserState.growth.set()


# проверяем переданные данные о росте, если корректно, запускаем функцию set_weight, если нет просим ввести данные заново

@dp.message_handler(state=UserState.growth)
async def chec_growth(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    if try_int(data['growth']):
        await set_weight(message, state, data=data)
    else:
        await message.answer('Рост введен не корректно, попробуйте еще раз.')
        await set_growth(message, state, data)


# если в дате есть информация о росте запрашиваем вес, если нет то добавляем рост и запрашиваем вес.

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state, data):
    if 'growth' in data.keys():
        await message.answer('Введите свой вес')
        await UserState.weight.set()
    else:
        await state.update_data(growth=message.text)
        data = await state.get_data()
        await message.answer('Введите свой вес')
        await UserState.weight.set()


# проверяем вес, если вес корректный, то запускаем функцию set_weight, если нет просим ввести вес еще раз

@dp.message_handler(state=UserState.weight)
async def chec_weight(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if try_int(data['weight']):
        await send_calories(message, state, data=data)
    else:
        await message.answer('Вес введен не корректно, попробуйте еще раз.')
        await set_weight(message, state, data)


# производим расчет нормы каллориев и отправляем ее пользователю

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state, data):
    women_cal = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    men_cal = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {men_cal}')
    await state.finish()


def input_info(file):
    with open(file, 'r') as f:
        result = f.read()
    return result


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer(input_info('info.txt'))


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_massage(message):
    await message.answer('Введите команду /start, чтобы начать общение.', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
