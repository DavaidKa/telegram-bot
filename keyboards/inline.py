from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎨 Создать мем", callback_data="create_meme"),
        InlineKeyboardButton(text="🎮 Викторина", callback_data="quiz_menu")
    )
    builder.row(
        InlineKeyboardButton(text="🎲 Мини-игра", callback_data="mini_game"),
        InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_stats")
    )
    builder.row(
        InlineKeyboardButton(text="💎 VIP подписка", callback_data="vip_info"),
        InlineKeyboardButton(text="👥 Рефералы", callback_data="referral_info")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Топ пользователей", callback_data="leaderboard")
    )
    return builder.as_markup()


def vip_menu() -> InlineKeyboardMarkup:
    """Меню VIP подписки"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Купить VIP ($2/мес)", callback_data="buy_vip")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Донат", callback_data="donate")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="main_menu")
    )
    return builder.as_markup()


def payment_methods() -> InlineKeyboardMarkup:
    """Способы оплаты"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="PayPal", callback_data="pay_paypal")
    )
    builder.row(
        InlineKeyboardButton(text="YooMoney", callback_data="pay_yoomoney"),
        InlineKeyboardButton(text="QIWI", callback_data="pay_qiwi")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="vip_info")
    )
    return builder.as_markup()


def meme_templates() -> InlineKeyboardMarkup:
    """Шаблоны мемов"""
    builder = InlineKeyboardBuilder()
    templates = [
        ("Дрейк", "drake"),
        ("Отвлекся", "distracted"),
        ("Мозг", "brain"),
        ("Кнопки", "buttons"),
        ("Успех", "success"),
        ("Случайный", "random")
    ]
    
    for name, callback in templates:
        builder.row(InlineKeyboardButton(text=name, callback_data=f"meme_{callback}"))
    
    builder.row(InlineKeyboardButton(text="« Назад", callback_data="main_menu"))
    return builder.as_markup()


def quiz_categories() -> InlineKeyboardMarkup:
    """Категории викторин"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎬 Кино", callback_data="quiz_movies"),
        InlineKeyboardButton(text="🎵 Музыка", callback_data="quiz_music")
    )
    builder.row(
        InlineKeyboardButton(text="🌍 География", callback_data="quiz_geo"),
        InlineKeyboardButton(text="🔬 Наука", callback_data="quiz_science")
    )
    builder.row(
        InlineKeyboardButton(text="⚡ Случайная", callback_data="quiz_random")
    )
    builder.row(
        InlineKeyboardButton(text="« Назад", callback_data="main_menu")
    )
    return builder.as_markup()


def share_result(content_id: int) -> InlineKeyboardMarkup:
    """Кнопка поделиться результатом"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📤 Поделиться с друзьями",
            switch_inline_query=f"result_{content_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Создать еще", callback_data="create_meme")
    )
    return builder.as_markup()


def admin_menu() -> InlineKeyboardMarkup:
    """Админ панель"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast"),
        InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")
    )
    builder.row(
        InlineKeyboardButton(text="« Закрыть", callback_data="close")
    )
    return builder.as_markup()


def back_button() -> InlineKeyboardMarkup:
    """Кнопка назад"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="« Назад", callback_data="main_menu"))
    return builder.as_markup()


def close_button() -> InlineKeyboardMarkup:
    """Кнопка закрыть"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✖️ Закрыть", callback_data="close"))
    return builder.as_markup()
