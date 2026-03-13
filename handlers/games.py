from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.database import db
from services.quiz_service import quiz_service
from services.game_service import game_service
from keyboards.inline import quiz_categories, back_button
import json

router = Router()


class QuizStates(StatesGroup):
    in_quiz = State()


@router.callback_query(F.data == "quiz_menu")
async def quiz_menu(callback: CallbackQuery):
    """Меню викторин"""
    text = (
        "🎮 Викторины\n\n"
        "Выбери категорию и проверь свои знания!\n"
        "За правильные ответы получишь опыт 📈"
    )
    await callback.message.edit_text(text, reply_markup=quiz_categories())
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_"))
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """Начать викторину"""
    category = callback.data.split("_")[1]
    
    questions = quiz_service.get_quiz(category, count=5)
    
    if not questions:
        await callback.answer("❌ Викторины пока нет", show_alert=True)
        return
    
    await state.update_data(
        questions=questions,
        current_question=0,
        correct_answers=0,
        category=category
    )
    
    await state.set_state(QuizStates.in_quiz)
    await show_question(callback.message, state)
    await callback.answer()


async def show_question(message: Message, state: FSMContext):
    """Показать вопрос"""
    data = await state.get_data()
    questions = data["questions"]
    current = data["current_question"]
    
    if current >= len(questions):
        await finish_quiz(message, state)
        return
    
    question = questions[current]
    
    text = (
        f"❓ Вопрос {current + 1}/{len(questions)}\n\n"
        f"{question['question']}\n\n"
    )
    
    # Создаем кнопки с вариантами
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    
    for i, option in enumerate(question['options']):
        builder.row(
            InlineKeyboardButton(
                text=option,
                callback_data=f"answer_{i}"
            )
        )
    
    try:
        await message.edit_text(text, reply_markup=builder.as_markup())
    except:
        await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("answer_"), QuizStates.in_quiz)
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа"""
    answer_index = int(callback.data.split("_")[1])
    
    data = await state.get_data()
    questions = data["questions"]
    current = data["current_question"]
    correct_answers = data["correct_answers"]
    
    question = questions[current]
    is_correct = quiz_service.check_answer(question, answer_index)
    
    if is_correct:
        correct_answers += 1
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        correct_answer = question['options'][question['correct']]
        await callback.answer(f"❌ Неправильно! Верный ответ: {correct_answer}", show_alert=True)
    
    await state.update_data(
        current_question=current + 1,
        correct_answers=correct_answers
    )
    
    await show_question(callback.message, state)


async def finish_quiz(message: Message, state: FSMContext):
    """Завершить викторину"""
    data = await state.get_data()
    correct = data["correct_answers"]
    total = len(data["questions"])
    
    result = quiz_service.calculate_score(correct, total)
    
    # Добавляем опыт
    user = await db.get_user(message.chat.id)
    exp_earned = correct * 15
    level_up = False
    
    if user:
        user.experience += exp_earned
        new_level = (user.experience // 100) + 1
        if new_level > user.level:
            user.level = new_level
            level_up = True
        await db.update_user(user)
    
    text = (
        f"{result['grade']}\n\n"
        f"📊 Результат: {correct}/{total} ({result['percentage']:.0f}%)\n"
        f"{result['message']}\n\n"
        f"⭐ Получено опыта: +{exp_earned}"
    )
    
    if level_up:
        text += f"\n\n🎉 Поздравляю! Ты достиг {user.level} уровня!"
    
    await message.edit_text(text, reply_markup=back_button())
    await state.clear()


@router.callback_query(F.data == "mini_game")
async def mini_game_menu(callback: CallbackQuery):
    """Меню мини-игр"""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎲 Кости", callback_data="game_dice")
    )
    builder.row(
        InlineKeyboardButton(text="🪨📄✂️ Камень-ножницы-бумага", callback_data="game_rps")
    )
    builder.row(
        InlineKeyboardButton(text="🔮 Предсказание дня", callback_data="game_fortune")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="main_menu")
    )
    
    text = (
        "🎮 Мини-игры\n\n"
        "Играй и зарабатывай опыт!\n"
        "Каждая игра дает бонусы 🎁"
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "game_dice")
async def play_dice_game(callback: CallbackQuery):
    """Игра в кости"""
    result = game_service.play_dice()
    
    user = await db.get_user(callback.from_user.id)
    if user:
        user.experience += result['exp']
        await db.update_user(user)
    
    text = (
        f"🎲 Игра в кости\n\n"
        f"{result['message']}\n\n"
        f"⭐ Опыт: +{result['exp']}"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Играть еще", callback_data="game_dice")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="mini_game")
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "game_rps")
async def rps_game_menu(callback: CallbackQuery):
    """Меню камень-ножницы-бумага"""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🪨 Камень", callback_data="rps_rock"),
        InlineKeyboardButton(text="📄 Бумага", callback_data="rps_paper")
    )
    builder.row(
        InlineKeyboardButton(text="✂️ Ножницы", callback_data="rps_scissors")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="mini_game")
    )
    
    await callback.message.edit_text(
        "🪨📄✂️ Выбери свой ход:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("rps_"))
async def play_rps_game(callback: CallbackQuery):
    """Игра камень-ножницы-бумага"""
    choice = callback.data.split("_")[1]
    result = game_service.play_rps(choice)
    
    user = await db.get_user(callback.from_user.id)
    if user:
        user.experience += result['exp']
        await db.update_user(user)
    
    text = (
        f"🪨📄✂️ Камень-ножницы-бумага\n\n"
        f"{result['message']}\n\n"
        f"⭐ Опыт: +{result['exp']}"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Играть еще", callback_data="game_rps")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="mini_game")
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "game_fortune")
async def daily_fortune(callback: CallbackQuery):
    """Предсказание дня"""
    fortune = game_service.daily_fortune()
    
    user = await db.get_user(callback.from_user.id)
    if user:
        user.experience += 10
        await db.update_user(user)
    
    text = (
        f"🔮 Предсказание дня\n\n"
        f"{fortune}\n\n"
        f"⭐ Опыт: +10"
    )
    
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()


from aiogram.types import InlineKeyboardButton
