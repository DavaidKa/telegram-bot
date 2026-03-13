from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.database import get_user
from services.ai_tutor import ai_tutor
from services.photo_solver import photo_solver
from utils.logger import logger

router = Router()


class ExamStates(StatesGroup):
    waiting_for_question = State()


@router.message(Command("exam"))
async def cmd_exam(message: Message, state: FSMContext):
    """Команда для помощи на контрольной"""
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Ошибка. Используйте /start для регистрации.")
        return
    
    # Проверяем лимиты для бесплатных пользователей
    if not user.is_vip_active():
        from database.database import get_today_requests_count
        requests_today = await get_today_requests_count(user.id)
        
        if requests_today >= 5:
            await message.answer(
                "❌ Вы исчерпали дневной лимит (5 запросов).\n\n"
                "💎 Оформите VIP подписку для безлимитного доступа: /premium"
            )
            return
    
    await message.answer(
        "📝 Режим помощи с контрольной активирован.\n\n"
        "Ты можешь:\n"
        "• отправить текст вопроса\n"
        "• отправить фото задания\n\n"
        "Ответы будут короткими, без объяснений."
    )
    await state.set_state(ExamStates.waiting_for_question)


@router.message(ExamStates.waiting_for_question, F.text)
async def process_exam_text(message: Message, state: FSMContext):
    """Обработка текстового вопроса на контрольной"""
    await message.answer("🤔 Думаю...")
    
    try:
        # Получаем короткий ответ от AI
        answer = await ai_tutor.solve_exam(message.text)
        
        # Сохраняем запрос
        from database.database import save_tutor_request
        await save_tutor_request(
            user_id=message.from_user.id,
            request_type="exam",
            question=message.text,
            answer=answer
        )
        
        await message.answer(answer)
        
    except Exception as e:
        logger.error(f"Error processing exam question: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
    
    finally:
        await state.clear()


@router.message(ExamStates.waiting_for_question, F.photo)
async def process_exam_photo(message: Message, state: FSMContext):
    """Обработка фото на контрольной"""
    # Проверяем VIP для фото
    user = await get_user(message.from_user.id)
    if not user.is_vip_active():
        await message.answer(
            "❌ Решение по фото доступно только VIP пользователям.\n\n"
            "💎 Оформите VIP: /premium"
        )
        await state.clear()
        return
    
    await message.answer("🔍 Распознаю...")
    
    try:
        # Скачиваем фото
        photo = message.photo[-1]
        bot = message.bot
        file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file.file_path)
        image_data = photo_bytes.read()
        
        # Распознаем текст
        text = await photo_solver.extract_text_from_image(image_data)
        
        if not text:
            await message.answer("❌ Не удалось распознать текст.")
            await state.clear()
            return
        
        # Получаем короткий ответ
        answer = await ai_tutor.solve_exam(text)
        
        # Сохраняем запрос
        from database.database import save_tutor_request
        await save_tutor_request(
            user_id=message.from_user.id,
            request_type="exam",
            question=f"[Photo] {text}",
            answer=answer
        )
        
        await message.answer(f"📷 Вопрос: {text}\n\n{answer}")
        
    except Exception as e:
        logger.error(f"Error processing exam photo: {e}")
        await message.answer("❌ Произошла ошибка.")
    
    finally:
        await state.clear()
