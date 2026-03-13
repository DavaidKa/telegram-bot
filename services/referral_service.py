from datetime import datetime, timedelta
from typing import Optional
from database.database import get_user, update_user
from utils.logger import logger


class ReferralService:
    """Сервис для работы с реферальной системой"""
    
    def __init__(self, bot_username: str = "YourBot"):
        self.bot_username = bot_username
    
    def generate_referral_link(self, user_id: int) -> str:
        """
        Генерация реферальной ссылки для пользователя
        
        Args:
            user_id: Telegram ID пользователя
        
        Returns:
            Реферальная ссылка
        """
        return f"https://t.me/{self.bot_username}?start={user_id}"
    
    async def process_referral(self, referrer_id: int, new_user_id: int) -> bool:
        """
        Обработка реферала
        
        Args:
            referrer_id: ID пригласившего пользователя
            new_user_id: ID нового пользователя
        
        Returns:
            True если реферал успешно обработан
        """
        try:
            # Проверяем, что пользователь не приглашает сам себя
            if referrer_id == new_user_id:
                return False
            
            # Получаем пригласившего пользователя
            referrer = await get_user(referrer_id)
            if not referrer:
                return False
            
            # Увеличиваем счетчик рефералов
            referrer.referral_count += 1
            
            # Добавляем 1 день VIP
            if referrer.is_vip and referrer.vip_until:
                referrer.vip_until += timedelta(days=1)
            else:
                referrer.is_vip = True
                referrer.vip_until = datetime.utcnow() + timedelta(days=1)
            
            await update_user(referrer)
            
            logger.info(f"Referral processed: {referrer_id} invited {new_user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing referral: {e}")
            return False
    
    async def get_referral_stats(self, user_id: int) -> dict:
        """
        Получить статистику рефералов пользователя
        
        Args:
            user_id: Telegram ID пользователя
        
        Returns:
            Словарь со статистикой
        """
        user = await get_user(user_id)
        if not user:
            return {"count": 0, "bonus_days": 0}
        
        return {
            "count": user.referral_count,
            "bonus_days": user.referral_count  # 1 день за каждого реферала
        }


# Глобальный экземпляр сервиса
referral_service = ReferralService()
