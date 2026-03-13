import aiohttp
import asyncio
from typing import Optional
from config import settings
from utils.logger import logger


class AITutor:
    """Сервис для работы с AI моделью через Hugging Face API"""
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        self.headers = {"Authorization": f"Bearer {settings.AI_API_KEY}"}
        self.max_retries = 3
        self.timeout = 30
    
    async def ask_ai(self, prompt: str, mode: str = "homework") -> Optional[str]:
        """
        Отправить запрос к AI модели
        
        Args:
            prompt: Вопрос пользователя
            mode: Режим работы (homework, exam)
        
        Returns:
            Ответ AI модели или None при ошибке
        """
        # Проверка наличия API ключа
        if not settings.AI_API_KEY or settings.AI_API_KEY == "":
            logger.error("AI_API_KEY not configured")
            return "❌ AI сервис временно недоступен. Обратитесь к администратору."
        
        # Формируем системный промпт в зависимости от режима
        if mode == "exam":
            system_prompt = "You are a helpful tutor. Give short, direct answers without explanations. Answer in Russian."
            full_prompt = f"{system_prompt}\n\nQuestion: {prompt}\n\nAnswer:"
        else:
            system_prompt = "You are a helpful tutor. Explain step by step in Russian."
            full_prompt = f"{system_prompt}\n\nQuestion: {prompt}\n\nProvide detailed solution and explanation:"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        # Попытки с повторами
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.api_url,
                        headers=self.headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            if isinstance(result, list) and len(result) > 0:
                                answer = result[0].get("generated_text", "").strip()
                                if answer:
                                    logger.info(f"AI response received (attempt {attempt + 1})")
                                    return answer
                            return "❌ Не удалось получить ответ от AI."
                        
                        elif response.status == 503:
                            # Модель загружается
                            error_data = await response.json()
                            if "estimated_time" in error_data:
                                wait_time = error_data["estimated_time"]
                                logger.warning(f"Model loading, wait {wait_time}s")
                                return f"⏳ AI модель загружается. Попробуйте через {int(wait_time)} секунд."
                        
                        elif response.status == 429:
                            # Rate limit
                            logger.warning("Rate limit exceeded")
                            return "⏳ Слишком много запросов. Попробуйте через минуту."
                        
                        else:
                            error_text = await response.text()
                            logger.error(f"AI API error: {response.status} - {error_text}")
                            
                            if attempt < self.max_retries - 1:
                                continue  # Retry
                            return "❌ Ошибка AI сервиса. Попробуйте позже."
            
            except asyncio.TimeoutError:
                logger.error(f"AI API timeout (attempt {attempt + 1})")
                if attempt < self.max_retries - 1:
                    continue
                return "⏳ AI сервис не отвечает. Попробуйте позже."
            
            except Exception as e:
                logger.error(f"Error calling AI API: {e}")
                if attempt < self.max_retries - 1:
                    continue
                return "❌ Произошла ошибка. Попробуйте позже."
        
        return "❌ Не удалось получить ответ после нескольких попыток."
    
    async def solve_homework(self, question: str) -> str:
        """
        Решить домашнее задание с подробным объяснением
        
        Args:
            question: Вопрос от пользователя
        
        Returns:
            Форматированный ответ
        """
        answer = await self.ask_ai(question, mode="homework")
        
        if not answer or answer.startswith("❌") or answer.startswith("⏳"):
            return answer
        
        # Форматируем ответ
        return f"📚 Решение:\n\n{answer}"
    
    async def solve_exam(self, question: str) -> str:
        """
        Быстрый ответ для контрольной (без объяснений)
        
        Args:
            question: Вопрос от пользователя
        
        Returns:
            Короткий ответ
        """
        answer = await self.ask_ai(question, mode="exam")
        
        if not answer or answer.startswith("❌") or answer.startswith("⏳"):
            return answer
        
        return f"✅ Ответ: {answer}"


# Глобальный экземпляр сервиса
ai_tutor = AITutor()
