from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from app.questions import questions
import app.keyboards as kb

router = Router() #создание роутера, в который добавляются все обработчики сообщений
user_data = {} #создание словаря для хранения данных пользователя


@router.message(F.text.in_(["/start", "Старт"]))
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Я телеграм бот для решения тестов по школьным предметам.\n'
        'Выберите предмет для теста:',
        reply_markup=kb.main
    ) #обработка команды старт и вывод клавиаторы с предметами

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('Вы нажали кнопку помощи')

@router.message(F.text.in_(['Русский язык', 'Математика', 'Обществознание', 'География', 'Информатика', 'Биология', 'Химия', 'Литература', 'История', 'Физика'])) #обработка выбора предмета
async def choose_subject(message: Message): #функция выбора предмета
    subject = message.text #сохранение названия предмета
    user_data[message.from_user.id] = {'subject': subject} #сохранение выбора предмета
    kb_dict = {
        'Русский язык': kb.rus,
        'Математика': kb.mat,
        'Обществознание': kb.obch,
        'География': kb.geo,
        'Информатика': kb.inf,
        'Биология': kb.bio,
        'Химия': kb.chim,
        'Литература': kb.lit,
        'История': kb.ist,
        'Физика': kb.fiz
    }
    await message.answer('Выберите уровень сложности', reply_markup=kb_dict[subject]) #отправка клавиатуры уровней

@router.callback_query(F.data.in_(['Easy level', 'Average level', 'Difficult level'])) #обработка выбора уровня
async def choose_level(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data: #проверка выбрал ли пользователь предмет
        await callback.message.answer("Сначала выберите предмет")
        return
    user_data[user_id]['level'] = callback.data #сохранение выбора уровня сложности
    user_data[user_id]['question_index'] = 0 #начало с первого вопроса
    user_data[user_id]['score'] = 0 #обнуление счета
    await callback.message.answer(f"Викторина началась! Уровень: {callback.data} 🚀") #старт викторины
    await send_question(callback.message, user_id) #отправка первого вопроса

async def send_question(message, user_id): #функция отправки первого вопроса
    data = user_data[user_id] #получение данных пользователя о предмете, уровне и номере вопроса
    subject = data['subject']
    level = data['level']
    index = data['question_index']

    q = questions[subject][level][index] #получение нужного вопроса из словаря
    data['correct_answer'] = q['answer'] #сохранение правильного ответа
    data['explanation'] = q['explanation'] #сохранение объяснения

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q['options']],
        resize_keyboard=True #создание клавиатуры с вариантами ответов
    )

    await message.answer(
        f"Вопрос {index + 1}:\n\n{q['question']}",
        reply_markup=keyboard #отправление вопроса пользователю
    )
@router.message() #получение любого текста отправленного пользователем
async def check_answer(message: Message): #проверка ответа
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    data = user_data[user_id]
    subject = data['subject']
    level = data['level']

    if message.text == data['correct_answer']: #проверка правильности ответа
        data['score'] += 1 #увеличение счета пользователя
        await message.answer("✅ Правильно!") #отправка сообщения о правильности ответа
    else:
        await message.answer(
            f"❌ Неправильно\n"
            f"✅ Правильный ответ: {data['correct_answer']}\n\n"
            f"📘 {data['explanation']}"
        ) #отправка сообщения об ошибке и объяснения

    data['question_index'] += 1 #переход к следующему вопросу
    if data['question_index'] < len(questions[subject][level]):
        await send_question(message, user_id) #если вопросы ещё есть отправка следующего вопроса
    else:
        await message.answer(
            f"🎉 Тест завершён!\n"
            f"Ваш результат: {data['score']} из {len(questions[subject][level])}",
            reply_markup = ReplyKeyboardRemove() # если вопросы закончились отправка результата и удаление клавиатуры ответов
        )
        await message.answer('Выберите предмет для нового теста:', reply_markup=kb.main) #отправка меню предметов
