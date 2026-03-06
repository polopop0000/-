from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Русский язык'),
                                      KeyboardButton(text='Математика')],
                                     [KeyboardButton(text='Обществознание'),
                                      KeyboardButton(text='География')],
                                     [KeyboardButton(text='Информатика'),
                                      KeyboardButton(text='Биология')],
                                     [KeyboardButton(text='Химия'),
                                      KeyboardButton(text='Литература')],
                                     [KeyboardButton(text='История'),
                                      KeyboardButton(text='Физика')]], #Создание главного меню бота
                           resize_keyboard=True, #Клавиатура становиться компактной
                           input_field_placeholder='Выберите предмет для теста...') #подсказка для пользователя в поле ввода
def level_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[ #функция возвращения клавиатуры
        [InlineKeyboardButton(text='Легкий уровень', callback_data='Easy level')],
        [InlineKeyboardButton(text='Средний уровень', callback_data='Average level')],
        [InlineKeyboardButton(text='Сложный уровень', callback_data='Difficult level')] #Создание кнопок уровней
    ])

rus = level_keyboard()
mat = level_keyboard()
obch = level_keyboard()
geo = level_keyboard()
inf = level_keyboard()
bio = level_keyboard()
chim = level_keyboard()
lit = level_keyboard()
ist = level_keyboard()
fiz = level_keyboard() #Клавиатура для предметов
