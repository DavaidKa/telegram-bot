from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from database.database import db
from keyboards.inline import back_button
from config import settings

router = Router()


@router.callback_query(F.data == "referral_info")
async def referral_info(callback: CallbackQuery):
    """Информация о реферальной программе"""
    user = await db.get_user(callback.from_user.id)
    
    bot_username = (await callback.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={callback.from_user.id}"
    
    text = (
        "👥 Реферальная программа\n\n"
        "🎁 Приглашай друзей и получай бонусы!\n\n"
        "За каждого приглашенного друга:\n"
        f"✅ {settings.REFERRAL_BONUS_DAYS} дня VIP бесплатно\n"
        "✅ +50 опыта\n"
        "✅ Бонусы для друга\n\n"
        f"👥 Твои рефералы: {user.referral_count}\n\n"
        f"🔗 Твоя реферальная ссылка:\n"
        f"`{referral_link}`\n\n"
        "💡 Отправь эту ссылку друзьям!"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📤 Поделиться ссылкой",
            switch_inline_query=f"Присоединяйся к крутому боту! {referral_link}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Топ рефералов", callback_data="top_referrers")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="main_menu")
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "top_referrers")
async def top_referrers(callback: CallbackQuery):
    """Топ рефералов"""
    from sqlalchemy import select
    from database.models import User
    from database.database import async_session_maker
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).order_by(User.referral_count.desc()).limit(10)
        )
        top_users = result.scalars().all()
    
    text = "🏆 Топ-10 рефералов\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(top_users, 1):
        if user.referral_count == 0:
            continue
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = user.first_name or user.username or "Аноним"
        text += f"{medal} {name} - {user.referral_count} рефералов\n"
    
    if not any(u.referral_count > 0 for u in top_users):
        text += "\nПока никто не пригласил друзей.\nСтань первым! 🚀"
    
    text += "\n\n💡 Приглашай друзей и получай бонусы!"
    
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()


@router.message(Command("referral"))
async def cmd_referral(message: Message):
    """Команда /referral"""
    user = await db.get_user(message.from_user.id)
    
    bot_username = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
    
    text = (
        "👥 Твоя реферальная ссылка\n\n"
        f"🔗 {referral_link}\n\n"
        f"👥 Приглашено друзей: {user.referral_count}\n"
        f"🎁 За каждого друга: {settings.REFERRAL_BONUS_DAYS} дня VIP\n\n"
        "📤 Поделись ссылкой с друзьями!"
    )
    
    await message.answer(text)


from aiogram.types import InlineKeyboardButton
