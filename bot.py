import os
from pathlib import Path
from config import TOKEN, SUPER_USER_ID
from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
# User classs
from database import Database
from markup import Keyboards
from states import StateBot, make_dir
from datetime import datetime

bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
db = Database(db_file_name='database.db')
kb = Keyboards()

# @dp.message_handler(commands = ['make_admin'],state=None)
# async def make_admin(message: types.Message):
#     if db.make_admin(int(message.text.split()[1])):
#         await message.answer(f'Права пользователя {int(message.text.split()[1])} изменены',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
#     else:
#         await message.answer(f'Невозможно изменение прав пользователя {int(message.text.split()[1])}',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    await message.answer('Запрос на добавление в список доверенных пользователей отправлен администратору.')
    await bot.send_message(SUPER_USER_ID,f'Добавить пользователя в доверенные пользователи?\nid = {message.from_user.id}\nname = {message.from_user.username}',reply_markup=kb.inline_add_user_buttons(message.from_user.id,message.from_user.username))
    
 
@dp.callback_query_handler(text_contains="useradd_")
async def add_question(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer,id,name = bool(int(call.data.split('_')[1])),int(call.data.split('_')[2]), str(call.data.split('_')[3])
    print(answer,id,name)
    if answer:
        await bot.send_message(id,'Доступ разрешен',reply_markup = kb.keyboard_main_buttons())
        await bot.send_message(SUPER_USER_ID,f'Пользователь\nid={id}\nname={name}\nДобавлен в список разрешенных пользователей')
        db.create_user(id, name)
    else:
        await bot.send_message(id,'Вам отказано в доступе к боту')

@dp.message_handler(Text(equals='Добавить инцидент'))
async def add_incident(message: types.Message, state: FSMContext):
    await state.finish() 
    await message.answer('Отправьте мне текст инцидента (ссылки и т.п.) одним сообщением')
    await StateBot.get_text.set()

# Обработки состояния принятия текста
@dp.message_handler(state=StateBot.get_text)
async def state_get_text(message: types.Message,state: FSMContext):
    StateBot.created_id = db.create_incident(incedent_text=message.text)
    await message.answer('Текст инцидента принят.\nОтправьте мне необходимые фотографии для добавления.\nПосле того как отправите все фотографии нажмите "Создать индцидент".\nЕсли прикреплять фотографии нет необходимости нажмите "Создать инцидент".',reply_markup=kb.inline_create_incident(StateBot.created_id))
    await state.finish()
    StateBot.get_photo = True

# Обработки состояния принятия фоток
# @dp.message_handler(state=StateBot.get_photo)
# async def state_get_text(message: types.Message,state: FSMContext):
#     await message.photo[-1].download('test.jpg')

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    if StateBot.get_photo:
        make_dir(StateBot.created_id)
        for photo_id in range(3,len(message.photo),4):
            await message.photo[photo_id].download(Path(os.getcwd(),str(StateBot.created_id),f"{datetime.now().microsecond}.jpg"))
        # await message.photo[-1].download(Path(os.getcwd(),str(StateBot.created_id),f"{datetime.now().microsecond}.jpg"))
        # await message.answer(f'Фотография №{len(os.listdir(Path(os.getcwd(),str(StateBot.created_id))))} принята')
        await message.answer(f'Фотография принята')
        # print(len(os.listdir(Path(os.getcwd(),str(StateBot.created_id)))))
    else:
        print('Состояние не подходит')

@dp.callback_query_handler(text_contains="create_")
async def add_question(call: types.CallbackQuery):
    StateBot.get_photo = False
    await bot.delete_message(call.from_user.id, call.message.message_id)
    incident_id = call.data.split('_')[1]
    db.add_photos(incident_id=incident_id)
    await bot.send_message(call.from_user.id,f'Инцидент с id={incident_id} добавлен в базу.')
    

@dp.message_handler(Text(equals='Показать инциденты'))
async def show_incident(message: types.Message, state: FSMContext):
    all_incidents = db.get_incidents()
    await message.answer('Выберите необходимый инцидент',reply_markup=kb.inline_all_incidents(all_incidents))

@dp.callback_query_handler(text_contains="incident_")
async def get_incident(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    current_incident_id = call.data.split("_")[1]
    text, photos = db.get_current_incident(current_incident_id)
    await bot.send_message(call.from_user.id,text[0],reply_markup=kb.inline_delete_incident(current_incident_id))
    for img in photos:
        await bot.send_photo(call.from_user.id,photo=img[0])

@dp.callback_query_handler(text_contains="delete_")
async def add_question(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    current_incident_id = call.data.split("_")[1]
    db.delete_incident(current_incident_id)

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)