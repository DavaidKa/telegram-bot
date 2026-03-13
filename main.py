import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from database.database import init_db
from utils.logger import logger
from middlewares.throttling import ThrottlingMiddleware
from services.notification import notification_service

# Импорт роутеров
from handlers import start, content, games, premium, referral, admin


async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    logger.info("Инициализация базы данных...")
    await init_db()
    
    logger.info("База данных инициализирована")
    
    # Уведомляем админов о запуске
    for admin_id in settings.admin_list:
        try:
            await bot.send_message(
                admin_id,
                "🤖 Бот запущен и готов к работе!"
            )
        except Exception as e:
            logger.error(f"Не удалось уведомить админа {admin_id}: {e}")


async def on_shutdown(bot: Bot):
    """Действия при остановке бота"""
    logger.info("Бот остановлен")


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Настройка планировщика задач"""
    scheduler = AsyncIOScheduler()
    
    # Ежедневный контент в 9:00
    scheduler.add_job(
        notification_service.send_daily_content,
        'cron',
        hour=9,
        minute=0,
        args=[bot]
    )
    
    # Викторина дня в 14:00
    scheduler.add_job(
        notification_service.send_daily_quiz,
        'cron',
        hour=14,
        minute=0,
        args=[bot]
    )
    
    # Предсказание в 20:00
    scheduler.add_job(
        notification_service.send_fortune,
        'cron',
        hour=20,
        minute=0,
        args=[bot]
    )
    
    # Проверка истечения VIP каждый день в 10:00
    scheduler.add_job(
        notification_service.notify_vip_expiring,
        'cron',
        hour=10,
        minute=0,
        args=[bot]
    )
    
    return scheduler


async def main():
    """Главная функция"""
    logger.info("Запуск бота...")
    
    # Запуск health check сервера для Render.com
    try:
        from render_health import start_health_server
        asyncio.create_task(start_health_server())
        logger.info("Health check сервер для Render запущен")
    except Exception as e:
        logger.warning(f"Health check сервер не запущен: {e}")
    
    # Инициализация бота
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    # Регистрация middleware
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    
    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(content.router)
    dp.include_router(games.router)
    dp.include_router(premium.router)
    dp.include_router(referral.router)
    dp.include_router(admin.router)
    
    # Регистрация событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Настройка планировщика
    scheduler = setup_scheduler(bot)
    scheduler.start()
    
    logger.info("Бот успешно запущен!")
    
    try:
        # Запуск polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
        sys.exit(0)
