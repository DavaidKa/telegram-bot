from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.database import db
from keyboards.inline import main_menu
from config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработка команды /start"""
    await state.clear()
    
    # Проверяем реферальную ссылку
    referrer_id = None
    if message.text and len(message.text.split()) > 1:
        try:
            referrer_id = int(message.text.split()[1])
        except:
            pass
    
    # Получаем или создаем пользователя
    user = await db.get_user(message.from_user.id)
    
    if not user:
        user = await db.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            referrer_id=referrer_id
        )
        
        welcome_text = (
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            "🎨 Я помогу тебе создавать крутые мемы, играть в викторины и мини-игры!\n\n"
            "✨ Что я умею:\n"
            "• Генерировать мемы и картинки\n"
            "• Викторины по разным темам\n"
            "• Мини-игры с призами\n"
            "• Система уровней и достижений\n\n"
            "🎁 Бесплатно: 5 генераций в день\n"
            "💎 VIP: безлимит за $2/мес\n\n"
            "👥 Приглашай друзей и получай бонусы!"
        )
        
        if referrer_id:
            welcome_text += "\n\n🎉 Ты пришел по реферальной ссылке! Твой друг получил бонус!"
    else:
        welcome_text = (
            f"С возвращением, {message.from_user.first_name}! 👋\n\n"
            f"📊 Твой уровень: {user.level}\n"
            f"⭐ Опыт: {user.experience}\n"
            f"🎨 Создано: {user.total_generated}\n"
        )
        
        if user.is_vip_active():
            welcome_text += f"\n💎 VIP активен до: {user.vip_until.strftime('%d.%m.%Y')}"
        else:
            welcome_text += f"\n🎁 Осталось генераций сегодня: {settings.FREE_DAILY_LIMIT - user.daily_usage}"
    
    await message.answer(welcome_text, reply_markup=main_menu())


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery):
    """Показать главное меню"""
    user = await db.get_user(callback.from_user.id)
    
    text = (
        "🎯 Главное меню\n\n"
        f"📊 Уровень: {user.level} | ⭐ Опыт: {user.experience}\n"
        f"🎨 Создано: {user.total_generated}\n"
    )
    
    if user.is_vip_active():
        text += f"💎 VIP до: {user.vip_until.strftime('%d.%m.%Y')}"
    else:
        text += f"🎁 Генераций сегодня: {settings.FREE_DAILY_LIMIT - user.daily_usage}/{settings.FREE_DAILY_LIMIT}"
    
    await callback.message.edit_text(text, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "my_stats")
async def show_stats(callback: CallbackQuery):
    """Показать статистику пользователя"""
    stats = await db.get_user_stats(callback.from_user.id)
    
    text = (
        "📊 Твоя статистика\n\n"
        f"🎯 Уровень: {stats['level']}\n"
        f"⭐ Опыт: {stats['experience']}\n"
        f"🎨 Всего создано: {stats['total_generated']}\n"
        f"👥 Рефералов: {stats['referrals']}\n"
    )
    
    if stats['is_vip']:
        text += f"\n💎 VIP статус: активен до {stats['vip_until']}"
    else:
        text += "\n💎 VIP статус: не активен"
    
    from keyboards.inline import back_button
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()


@router.callback_query(F.data == "close")
async def close_message(callback: CallbackQuery):
    """Закрыть сообщение"""
    await callback.message.delete()
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Помощь"""
    help_text = (
        "ℹ️ Помощь\n\n"
        "📝 Команды:\n"
        "/start - Главное меню\n"
        "/help - Эта справка\n"
        "/stats - Твоя статистика\n"
        "/referral - Реферальная ссылка\n"
        "/vip - Информация о VIP\n\n"
        "💡 Как работает бот:\n"
        "1. Создавай мемы и контент\n"
        "2. Играй в викторины и игры\n"
        "3. Получай опыт и повышай уровень\n"
        "4. Приглашай друзей за бонусы\n"
        "5. Покупай VIP для безлимита\n\n"
        "❓ Вопросы? Пиши @support"
    )
    
    await message.answer(help_text)


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика"""
    stats = await db.get_user_stats(message.from_user.id)
    
    text = (
        "📊 Твоя статистика\n\n"
        f"🎯 Уровень: {stats['level']}\n"
        f"⭐ Опыт: {stats['experience']}\n"
        f"🎨 Всего создано: {stats['total_generated']}\n"
        f"👥 Рефералов: {stats['referrals']}\n"
    )
    
    if stats['is_vip']:
        text += f"\n💎 VIP статус: активен до {stats['vip_until']}"
    else:
        text += "\n💎 VIP статус: не активен"
    
    await message.answer(text)
