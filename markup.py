from database import Database
from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType

class Keyboards:
    def keyboard_main_buttons(self) -> types.ReplyKeyboardMarkup:
        # main_button = ['Начать выдачу','Остановить выдачу'] #Раскоментить если рекурсивная выдача
        main_button = ['Добавить инцидент','Показать инциденты'] #Это закоментить
        # if user_id in self.db.get_admin_id():
        #     main_button.append('Добавить фото в БД')
        keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        keyboard_main.add(*main_button)
        return keyboard_main

    def inline_add_user_buttons(self, to_add_user_id, to_add_user_name):
        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
        true_button = types.InlineKeyboardButton(text='Да', callback_data=f'useradd_1_{to_add_user_id}_{to_add_user_name}')
        false_button = types.InlineKeyboardButton(text='Нет', callback_data=f'useradd_0_{to_add_user_id}_{to_add_user_name}')
        inline_keyboard.row(true_button,false_button)
        return inline_keyboard

    def inline_create_incident(self, incident_id):
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text='Создать инцидент', callback_data=f'create_{incident_id}'))
        return inline_keyboard

    def inline_all_incidents(self, data):
        inline_keyboard = types.InlineKeyboardMarkup()
        for row in data:
            inline_keyboard.add(types.InlineKeyboardButton(text=row[1], callback_data=f'incident_{row[0]}'))
        return inline_keyboard

    def inline_delete_incident(self, incident_id):
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text='Удалить инцидент', callback_data=f'delete_{incident_id}'))
        return inline_keyboard