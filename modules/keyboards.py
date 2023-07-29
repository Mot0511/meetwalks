from aiogram import *
from aiogram.types import *

kb_genre = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'))
kb_genre2 = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'), KeyboardButton('Не важно'))
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Искать людей'), KeyboardButton('Моя анкета'))
kb_edit = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Изменить анкету'), KeyboardButton('В главное меню'))
kb_select = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('✔'), KeyboardButton('✖')).add(KeyboardButton('В главное меню'))
kb_exit = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('В главное меню'))
kb_leave = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Покинуть компанию'))
kb_sendLocation = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить геолокацию', request_location=True))
kb_count = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'), KeyboardButton('5')).add(KeyboardButton('В главное меню'))

ikb_allow = InlineKeyboardMarkup().add(InlineKeyboardButton('Принять', callback_data='allow')).add(InlineKeyboardButton('Отклонить', callback_data='reject'))