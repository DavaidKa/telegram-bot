from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from database.database import db
from keyboards.inline import vip_menu, payment_methods, back_button
from config import settings

router = Router()


@router.callback_query(F.data == "vip_info")
async def vip_info(callback: CallbackQuery):
    """Информация о VIP"""
    user = await db.get_user(callback.from_user.id)
    
    text = (
        "💎 VIP подписка\n\n"
        "Преимущества VIP:\n"
        "✅ Безлимитная генерация контента\n"
        "✅ Эксклюзивные шаблоны мемов\n"
        "✅ Приоритетная поддержка\n"
        "✅ Специальный значок в рейтинге\n"
        "✅ Бонусный опыт за действия\n\n"
        f"💰 Цена: ${settings.VIP_PRICE_USD}/месяц\n\n"
    )
    
    if user.is_vip_active():
        text += f"✨ Твой VIP активен до: {user.vip_until.strftime('%d.%m.%Y')}"
    else:
        text += "🎁 Первая неделя со скидкой 50%!"
    
    await callback.message.edit_text(text, reply_markup=vip_menu())
    await callback.answer()


@router.callback_query(F.data == "buy_vip")
async def buy_vip(callback: CallbackQuery):
    """Купить VIP"""
    text = (
        "💳 Выбери способ оплаты\n\n"
        f"Сумма: ${settings.VIP_PRICE_USD}\n"
        "Период: 30 дней\n\n"
        "После оплаты VIP активируется автоматически"
    )
    
    await callback.message.edit_text(text, reply_markup=payment_methods())
    await callback.answer()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    """Обработка оплаты"""
    payment_system = callback.data.split("_")[1]
    user = await db.get_user(callback.from_user.id)
    
    # Создаем платеж в БД
    payment = await db.create_payment(
        user_id=user.id,
        amount=settings.VIP_PRICE_USD,
        payment_system=payment_system,
        payment_type="vip"
    )
    
    # Генерируем ссылку на оплату (заглушка)
    payment_links = {
        "paypal": f"https://paypal.me/yourbot/{settings.VIP_PRICE_USD}",
        "yoomoney": f"https://yoomoney.ru/to/410011234567890/{settings.VIP_PRICE_USD}",
        "qiwi": f"https://qiwi.com/payment/form/99?extra['account']=+79001234567&amountInteger={int(settings.VIP_PRICE_USD)}"
    }
    
    link = payment_links.get(payment_system, "#")
    
    text = (
        f"💳 Оплата через {payment_system.upper()}\n\n"
        f"Сумма: ${settings.VIP_PRICE_USD}\n"
        f"ID платежа: {payment.id}\n\n"
        f"Перейди по ссылке для оплаты:\n{link}\n\n"
        "⚠️ После оплаты VIP активируется автоматически в течение 5 минут.\n"
        "Если возникли проблемы - напиши @support"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Оплатить", url=link)
    )
    builder.row(
        InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_payment_{payment.id}")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="buy_vip")
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("check_payment_"))
async def check_payment(callback: CallbackQuery):
    """Проверка оплаты (заглушка)"""
    # В реальном боте здесь должна быть проверка через API платежной системы
    
    await callback.answer(
        "⏳ Проверяем оплату...\n"
        "Обычно это занимает 1-5 минут.\n"
        "Мы уведомим тебя когда VIP активируется!",
        show_alert=True
    )
    
    # Для демо активируем VIP сразу
    user = await db.get_user(callback.from_user.id)
    await db.activate_vip(callback.from_user.id, days=30)
    
    await callback.message.answer(
        "🎉 Поздравляем!\n\n"
        "💎 VIP подписка активирована на 30 дней!\n"
        "Теперь у тебя безлимитный доступ ко всем функциям!\n\n"
        "Спасибо за поддержку! ❤️"
    )


@router.callback_query(F.data == "donate")
async def donate_info(callback: CallbackQuery):
    """Информация о донатах"""
    text = (
        "💰 Поддержать проект\n\n"
        "Если тебе нравится бот, ты можешь поддержать его развитие!\n\n"
        "Любая сумма будет очень полезна:\n"
        "• Улучшение функций\n"
        "• Новые шаблоны и игры\n"
        "• Стабильная работа сервера\n\n"
        "🎁 За донат от $5 - неделя VIP в подарок!"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    
    donate_amounts = [1, 3, 5, 10]
    for amount in donate_amounts:
        builder.row(
            InlineKeyboardButton(
                text=f"💵 ${amount}",
                callback_data=f"donate_{amount}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="vip_info")
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("donate_"))
async def process_donation(callback: CallbackQuery):
    """Обработка доната"""
    amount = int(callback.data.split("_")[1])
    
    text = (
        f"💝 Донат ${amount}\n\n"
        "Спасибо за поддержку!\n\n"
        "Выбери способ оплаты:"
    )
    
    await callback.message.edit_text(text, reply_markup=payment_methods())
    await callback.answer()


from aiogram.types import InlineKeyboardButton
