from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.database import get_user
from services.photo_solver import photo_solver
from utils.logger import logger

router = Router()


class PhotoSolverStates(StatesGroup):
    waiting_for_photo = State()


@router.message(Command("solve"))
async def cmd_solve(message: Message, state: FSMContext):
    """Команда для решения задач по фото"""
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Ошибка. Используйте /start для регистрации.")
        return
    
    # Проверяем VIP статус (фото решение только для VIP)
    if not user.is_vip_active():
        await message.answer(
            "❌ Решение задач по фото доступно только VIP пользователям.\n\n"
            "💎 Оформите VIP подписку: /premium"
        )
        return
    
    await message.answer(
        "📷 Отправь фото задачи. Я распознаю текст и помогу решить."
    )
    await state.set_state(PhotoSolverStates.waiting_for_photo)


@router.message(PhotoSolverStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Обработка фото с задачей"""
    # Показываем, что бот работает
    await message.answer("🔍 Распознаю текст на фото...")
    
    try:
        # Получаем самое большое фото
        photo = message.photo[-1]
        
        # Скачиваем фото
        from aiogram import Bot
        bot = message.bot
        file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file.file_path)
        
        # Читаем байты
        image_data = photo_bytes.read()
        
        # Решаем задачу
        solution = await photo_solver.solve_from_photo(image_data)
        
        # Сохраняем запрос в базу данных
        from database.database import save_tutor_request
        await save_tutor_request(
            user_id=message.from_user.id,
            request_type="photo",
            question="[Photo]",
            answer=solution
        )
        
        # Отправляем ответ
        await message.answer(solution)
        
    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        await message.answer("❌ Произошла ошибка при обработке фото. Попробуйте позже.")
    
    finally:
        await state.clear()


@router.message(PhotoSolverStates.waiting_for_photo)
async def invalid_photo(message: Message):
    """Обработка неправильного ввода"""
    await message.answer("❌ Пожалуйста, отправьте фото задачи.")
