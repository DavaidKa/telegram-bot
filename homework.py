from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.database import get_user
from services.ai_tutor import ai_tutor
from utils.logger import logger

router = Router()


class HomeworkStates(StatesGroup):
    waiting_for_question = State()


@router.message(Command("homework"))
async def cmd_homework(message: Message, state: FSMContext):
    """Команда для помощи с домашним заданием"""
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Ошибка. Используйте /start для регистрации.")
        return
    
    # Проверяем лимиты для бесплатных пользователей
    if not user.is_vip_active():
        # Подсчитываем использованные запросы за сегодня
        from database.database import get_today_requests_count
        requests_today = await get_today_requests_count(message.from_user.id)
        
        if requests_today >= 5:
            await message.answer(
                "❌ Вы исчерпали дневной лимит (5 запросов).\n\n"
                "💎 Оформите VIP подписку для безлимитного доступа: /premium"
            )
            return
    
    await message.answer(
        "📚 Отправь вопрос по домашнему заданию. "
        "Я помогу решить задачу и объясню ответ."
    )
    await state.set_state(HomeworkStates.waiting_for_question)


@router.message(HomeworkStates.waiting_for_question)
async def process_homework_question(message: Message, state: FSMContext):
    """Обработка вопроса по домашнему заданию"""
    if not message.text:
        await message.answer("❌ Пожалуйста, отправьте текстовый вопрос.")
        return
    
    # Показываем, что бот работает
    processing_msg = await message.answer("🤔 Думаю над решением...")
    
    try:
        # Получаем решение от AI
        solution = await ai_tutor.solve_homework(message.text)
        
        # Сохраняем запрос в базу данных
        from database.database import save_tutor_request
        await save_tutor_request(
            user_id=message.from_user.id,
            request_type="homework",
            question=message.text,
            answer=solution
        )
        
        # Удаляем сообщение "Думаю..."
        await processing_msg.delete()
        
        # Отправляем ответ
        await message.answer(solution)
        
        logger.info(f"Homework solved for user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error processing homework: {e}")
        await processing_msg.delete()
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
    
    finally:
        await state.clear()
