from aiogram import Bot
from database.database import db
from services.meme_generator import meme_gen
from services.game_service import game_service
from utils.logger import logger
import random


class NotificationService:
    """Сервис уведомлений"""
    
    @staticmethod
    async def send_daily_content(bot: Bot):
        """Отправка ежедневного контента"""
        users = await db.get_all_users()
        
        logger.info(f"Отправка ежедневного контента для {len(users)} пользователей")
        
        # Мем дня
        quote, image = meme_gen.create_motivational_quote()
        
        success = 0
        failed = 0
        
        for user in users:
            try:
                # Отправляем только активным пользователям
                if user.total_generated > 0:
                    from aiogram.types import BufferedInputFile
                    
                    photo = BufferedInputFile(image, filename="daily_meme.png")
                    
                    await bot.send_photo(
                        chat_id=user.telegram_id,
                        photo=photo,
                        caption=(
                            f"🌅 Доброе утро!\n\n"
                            f"💫 {quote}\n\n"
                            f"Создай свой мем сегодня! /start"
                        )
                    )
                    success += 1
            except Exception as e:
                failed += 1
                logger.error(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
        
        logger.info(f"Рассылка завершена. Успешно: {success}, Ошибок: {failed}")
    
    @staticmethod
    async def send_daily_quiz(bot: Bot):
        """Отправка ежедневной викторины"""
        users = await db.get_all_users()
        
        logger.info(f"Отправка ежедневной викторины для {len(users)} пользователей")
        
        success = 0
        
        for user in users:
            try:
                if user.total_generated > 0:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=(
                            "🎮 Викторина дня!\n\n"
                            "Проверь свои знания и получи бонусный опыт!\n\n"
                            "Нажми /start и выбери 'Викторина'"
                        )
                    )
                    success += 1
            except Exception as e:
                logger.error(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
        
        logger.info(f"Рассылка викторин завершена. Успешно: {success}")
    
    @staticmethod
    async def send_fortune(bot: Bot):
        """Отправка предсказаний"""
        users = await db.get_all_users()
        
        logger.info(f"Отправка предсказаний для {len(users)} пользователей")
        
        for user in users:
            try:
                if user.total_generated > 0:
                    fortune = game_service.daily_fortune()
                    
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"🔮 Предсказание дня\n\n{fortune}"
                    )
            except Exception as e:
                logger.error(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
    
    @staticmethod
    async def notify_vip_expiring(bot: Bot):
        """Уведомление об истечении VIP"""
        from datetime import datetime, timedelta
        
        users = await db.get_all_users()
        
        # Уведомляем за 3 дня до истечения
        expiring_soon = datetime.utcnow() + timedelta(days=3)
        
        for user in users:
            if user.is_vip and user.vip_until:
                if user.vip_until.date() == expiring_soon.date():
                    try:
                        await bot.send_message(
                            chat_id=user.telegram_id,
                            text=(
                                "⚠️ Напоминание\n\n"
                                f"Твой VIP истекает через 3 дня ({user.vip_until.strftime('%d.%m.%Y')})\n\n"
                                "Продли подписку, чтобы не потерять преимущества!\n"
                                "/vip"
                            )
                        )
                    except Exception as e:
                        logger.error(f"Ошибка уведомления пользователя {user.telegram_id}: {e}")


notification_service = NotificationService()
