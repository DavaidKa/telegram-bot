"""
Health check сервер для Render.com

Render ожидает HTTP ответ на порту 10000.
Этот сервер отвечает на запросы и подтверждает что бот работает.
"""

from aiohttp import web
import logging

logger = logging.getLogger(__name__)


async def health_check(request):
    """Endpoint для проверки здоровья бота"""
    return web.Response(text="✅ Bot is running!", status=200)


async def start_health_server():
    """Запуск HTTP сервера для health checks"""
    try:
        app = web.Application()
        app.router.add_get('/', health_check)
        app.router.add_get('/health', health_check)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        # Render использует порт 10000 по умолчанию
        site = web.TCPSite(runner, '0.0.0.0', 10000)
        await site.start()
        
        logger.info("Health check сервер запущен на порту 10000")
    except Exception as e:
        logger.error(f"Ошибка запуска health check сервера: {e}")
