from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.database import db
from keyboards.inline import admin_menu, close_button
from config import settings

router = Router()


class BroadcastStates(StatesGroup):
    waiting_for_message = State()


def is_admin(user_id: int) -> bool:
    """Проверка на админа"""
    return user_id in settings.admin_list


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Админ панель"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У тебя нет доступа к админ-панели")
        return
    
    text = (
        "👨‍💼 Админ панель\n\n"
        "Управление ботом и пользователями"
    )
    
    await message.answer(text, reply_markup=admin_menu())


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Статистика бота"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    stats = await db.get_stats()
    
    text = (
        "📊 Статистика бота\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"💎 VIP пользователей: {stats['vip_users']}\n"
        f"💰 Всего платежей: {stats['total_payments']}\n"
        f"💵 Общий доход: ${stats['total_revenue']:.2f}\n"
    )
    
    await callback.message.edit_text(text, reply_markup=admin_menu())
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    """Рассылка"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    text = (
        "📢 Рассылка сообщений\n\n"
        "Отправь сообщение, которое хочешь разослать всем пользователям.\n\n"
        "⚠️ Используй с осторожностью!"
    )
    
    await callback.message.edit_text(text, reply_markup=close_button())
    await state.set_state(BroadcastStates.waiting_for_message)
    await callback.answer()


@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext):
    """Обработка рассылки"""
    if not is_admin(message.from_user.id):
        await state.clear()
        return
    
    users = await db.get_all_users()
    
    await message.answer(f"📤 Начинаю рассылку для {len(users)} пользователей...")
    
    success = 0
    failed = 0
    
    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user.telegram_id,
                text=message.text
            )
            success += 1
        except Exception as e:
            failed += 1
    
    result_text = (
        f"✅ Рассылка завершена!\n\n"
        f"Успешно: {success}\n"
        f"Ошибок: {failed}"
    )
    
    await message.answer(result_text)
    await state.clear()


@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    """Список пользователей"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    users = await db.get_all_users()
    
    # Показываем последних 10 пользователей
    recent_users = sorted(users, key=lambda x: x.created_at, reverse=True)[:10]
    
    text = "👥 Последние 10 пользователей:\n\n"
    
    for user in recent_users:
        name = user.first_name or user.username or "Аноним"
        vip_status = "💎" if user.is_vip_active() else ""
        text += (
            f"{vip_status} {name}\n"
            f"ID: {user.telegram_id}\n"
            f"Уровень: {user.level} | Опыт: {user.experience}\n"
            f"Создано: {user.total_generated}\n\n"
        )
    
    await callback.message.edit_text(text, reply_markup=admin_menu())
    await callback.answer()


@router.message(Command("give_vip"))
async def cmd_give_vip(message: Message):
    """Выдать VIP пользователю"""
    if not is_admin(message.from_user.id):
        return
    
    try:
        # Формат: /give_vip user_id days
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("Использование: /give_vip <user_id> [days=30]")
            return
        
        user_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else 30
        
        success = await db.activate_vip(user_id, days=days)
        
        if success:
            await message.answer(f"✅ VIP выдан пользователю {user_id} на {days} дней")
            
            # Уведомляем пользователя
            try:
                await message.bot.send_message(
                    chat_id=user_id,
                    text=f"🎉 Поздравляем!\n\nТебе выдан VIP статус на {days} дней!"
                )
            except:
                pass
        else:
            await message.answer("❌ Пользователь не найден")
    
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


@router.message(Command("stats_full"))
async def cmd_stats_full(message: Message):
    """Полная статистика"""
    if not is_admin(message.from_user.id):
        return
    
    stats = await db.get_stats()
    users = await db.get_all_users()
    
    # Дополнительная статистика
    active_today = sum(1 for u in users if u.last_usage_date.date() == message.date.date())
    total_content = sum(u.total_generated for u in users)
    avg_level = sum(u.level for u in users) / len(users) if users else 0
    
    text = (
        "📊 Полная статистика\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"📈 Активных сегодня: {active_today}\n"
        f"💎 VIP пользователей: {stats['vip_users']}\n"
        f"🎨 Всего создано контента: {total_content}\n"
        f"📊 Средний уровень: {avg_level:.1f}\n\n"
        f"💰 Финансы:\n"
        f"Платежей: {stats['total_payments']}\n"
        f"Доход: ${stats['total_revenue']:.2f}\n"
    )
    
    await message.answer(text)
