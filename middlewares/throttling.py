from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import time


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для защиты от спама"""
    
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.user_timestamps: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()
        
        # Проверяем последнее действие пользователя
        if user_id in self.user_timestamps:
            time_passed = current_time - self.user_timestamps[user_id]
            
            if time_passed < self.rate_limit:
                # Слишком быстро
                if isinstance(event, CallbackQuery):
                    await event.answer("⏳ Не так быстро!", show_alert=True)
                return
        
        # Обновляем время последнего действия
        self.user_timestamps[user_id] = current_time
        
        return await handler(event, data)
