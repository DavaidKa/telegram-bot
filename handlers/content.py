from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.database import db
from services.meme_generator import meme_gen
from keyboards.inline import meme_templates, share_result, back_button
from config import settings

router = Router()


class MemeStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_bottom_text = State()


@router.callback_query(F.data == "create_meme")
async def create_meme_menu(callback: CallbackQuery):
    """Меню создания мема"""
    user = await db.get_user(callback.from_user.id)
    
    if not user.can_generate(settings.FREE_DAILY_LIMIT):
        await callback.answer(
            "❌ Лимит исчерпан! Купи VIP или приглашай друзей за бонусы",
            show_alert=True
        )
        return
    
    text = (
        "🎨 Создание мема\n\n"
        "Выбери шаблон или создай свой мем с текстом!\n\n"
        "💡 Совет: Делись мемами с друзьями - они увидят ссылку на бота!"
    )
    
    await callback.message.edit_text(text, reply_markup=meme_templates())
    await callback.answer()


@router.callback_query(F.data.startswith("meme_"))
async def generate_meme(callback: CallbackQuery, state: FSMContext):
    """Генерация мема"""
    template = callback.data.split("_")[1]
    user = await db.get_user(callback.from_user.id)
    
    if not user.can_generate(settings.FREE_DAILY_LIMIT):
        await callback.answer("❌ Лимит исчерпан!", show_alert=True)
        return
    
    await callback.message.edit_text("⏳ Создаю мем...")
    
    try:
        if template == "random":
            image_bytes = meme_gen.create_random_meme()
            caption = "🎨 Случайный мем"
        else:
            # Для простоты создаем мотивационную цитату
            quote, image_bytes = meme_gen.create_motivational_quote()
            caption = f"💫 {quote}"
        
        # Сохраняем в БД
        content = await db.save_content(
            user_id=user.id,
            content_type="meme",
            prompt=template
        )
        
        # Обновляем счетчик
        level_up = await db.increment_usage(callback.from_user.id)
        
        # Отправляем мем
        photo = BufferedInputFile(image_bytes, filename="meme.png")
        await callback.message.delete()
        
        sent_message = await callback.message.answer_photo(
            photo=photo,
            caption=caption + "\n\n📤 Поделись с друзьями!",
            reply_markup=share_result(content.id)
        )
        
        if level_up:
            await callback.message.answer(
                f"🎉 Поздравляю! Ты достиг {user.level} уровня!"
            )
        
        await callback.answer("✅ Мем создан!")
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Ошибка при создании мема: {str(e)}",
            reply_markup=back_button()
        )
        await callback.answer()


@router.callback_query(F.data == "create_custom_meme")
async def create_custom_meme(callback: CallbackQuery, state: FSMContext):
    """Создать свой мем с текстом"""
    await callback.message.edit_text(
        "✍️ Отправь текст для верхней части мема:",
        reply_markup=back_button()
    )
    await state.set_state(MemeStates.waiting_for_text)
    await callback.answer()


@router.message(MemeStates.waiting_for_text)
async def process_meme_text(message: Message, state: FSMContext):
    """Обработка текста для мема"""
    await state.update_data(top_text=message.text)
    await message.answer(
        "✍️ Отлично! Теперь отправь текст для нижней части (или /skip чтобы пропустить):"
    )
    await state.set_state(MemeStates.waiting_for_bottom_text)


@router.message(MemeStates.waiting_for_bottom_text)
async def process_meme_bottom_text(message: Message, state: FSMContext):
    """Обработка нижнего текста"""
    data = await state.get_data()
    top_text = data.get("top_text", "")
    bottom_text = message.text if message.text != "/skip" else ""
    
    user = await db.get_user(message.from_user.id)
    
    if not user.can_generate(settings.FREE_DAILY_LIMIT):
        await message.answer("❌ Лимит исчерпан!")
        await state.clear()
        return
    
    await message.answer("⏳ Создаю твой мем...")
    
    try:
        image_bytes = meme_gen.create_simple_meme(top_text, bottom_text)
        
        content = await db.save_content(
            user_id=user.id,
            content_type="custom_meme",
            prompt=f"{top_text} | {bottom_text}"
        )
        
        level_up = await db.increment_usage(message.from_user.id)
        
        photo = BufferedInputFile(image_bytes, filename="meme.png")
        await message.answer_photo(
            photo=photo,
            caption="🎨 Твой мем готов!\n\n📤 Поделись с друзьями!",
            reply_markup=share_result(content.id)
        )
        
        if level_up:
            await message.answer(f"🎉 Поздравляю! Ты достиг {user.level} уровня!")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
    
    await state.clear()


@router.callback_query(F.data == "leaderboard")
async def show_leaderboard(callback: CallbackQuery):
    """Таблица лидеров"""
    top_users = await db.get_top_users(10)
    
    text = "🏆 Топ-10 пользователей\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(top_users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = user.first_name or user.username or "Аноним"
        text += f"{medal} {name} - Ур.{user.level} ({user.experience} опыта)\n"
    
    text += "\n💡 Создавай контент и приглашай друзей, чтобы попасть в топ!"
    
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()
