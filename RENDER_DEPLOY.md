# 🚀 Запуск на Render.com (РЕКОМЕНДУЮ!)

## ✅ Почему Render хороший выбор:

- ✅ **750 часов/месяц БЕСПЛАТНО** (больше чем Railway!)
- ✅ Не требует кредитную карту
- ✅ Простой деплой за 5 минут
- ✅ Автоматические обновления из GitHub
- ✅ Бесплатный SSL сертификат
- ⚠️ Засыпает после 15 минут неактивности (но легко решается)

---

## 📋 Пошаговая инструкция (5 минут)

### Шаг 1: Подготовка GitHub репозитория (2 минуты)

1. **Создайте аккаунт на GitHub** (если нет):
   - Перейдите на https://github.com
   - Нажмите "Sign up"

2. **Создайте новый репозиторий:**
   - Нажмите "+" → "New repository"
   - Название: `viral-telegram-bot`
   - Выберите "Public"
   - Нажмите "Create repository"

3. **Загрузите файлы проекта:**
   
   **Вариант A: Через веб-интерфейс (проще)**
   - Нажмите "uploading an existing file"
   - Перетащите ВСЕ файлы из папки `C:\Users\lohhh\Desktop\Тг Бот`
   - Нажмите "Commit changes"

   **Вариант B: Через Git (если установлен)**
   ```bash
   cd "C:\Users\lohhh\Desktop\Тг Бот"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/ваш-username/viral-telegram-bot.git
   git push -u origin main
   ```

---

### Шаг 2: Регистрация на Render (1 минута)

1. Перейдите на https://render.com
2. Нажмите "Get Started"
3. Войдите через GitHub (рекомендуется)
4. Разрешите доступ к репозиториям

---

### Шаг 3: Создание Web Service (2 минуты)

1. **В Dashboard нажмите "New +"**
2. **Выберите "Web Service"**
3. **Подключите репозиторий:**
   - Найдите `viral-telegram-bot`
   - Нажмите "Connect"

4. **Настройте сервис:**
   ```
   Name: viral-telegram-bot
   Region: Frankfurt (или ближайший к вам)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

5. **Выберите план:**
   - Выберите "Free" (750 часов/месяц)
   - Нажмите "Create Web Service"

---

### Шаг 4: Добавление переменных окружения (1 минута)

1. **В настройках сервиса найдите "Environment"**
2. **Нажмите "Add Environment Variable"**
3. **Добавьте переменные:**

```
BOT_TOKEN = 8742742015:AAFTS2z3y5MSYGvhwBymmGR7h3RAKpsZ5W0
DATABASE_URL = sqlite+aiosqlite:///data/bot.db
VIP_PRICE_USD = 2
REFERRAL_BONUS_DAYS = 3
FREE_DAILY_LIMIT = 5
LOG_LEVEL = INFO
```

4. **Нажмите "Save Changes"**

---

### Шаг 5: Деплой и проверка (1 минута)

1. **Render автоматически начнет деплой**
2. **Следите за логами:**
   - Должно появиться "Бот успешно запущен!"
   - Процесс займет 2-3 минуты

3. **Проверьте работу:**
   - Откройте Telegram
   - Найдите вашего бота
   - Отправьте `/start`
   - Работает! 🎉

---

## ⚠️ ВАЖНО: Решение проблемы засыпания

Render усыпляет бесплатные сервисы после 15 минут неактивности.

### Решение 1: UptimeRobot (РЕКОМЕНДУЮ)

1. **Зарегистрируйтесь на https://uptimerobot.com** (бесплатно)

2. **Создайте новый монитор:**
   - Нажмите "Add New Monitor"
   - Monitor Type: HTTP(s)
   - Friendly Name: Telegram Bot
   - URL: `https://ваш-сервис.onrender.com` (скопируйте из Render)
   - Monitoring Interval: 5 минут

3. **Сохраните**

Теперь UptimeRobot будет "пинговать" ваш бот каждые 5 минут, и он не будет засыпать!

### Решение 2: Cron-job.org

1. Зарегистрируйтесь на https://cron-job.org
2. Создайте задачу с URL вашего сервиса
3. Интервал: каждые 5 минут

---

## 🔧 Настройка для Telegram бота

Render ожидает HTTP сервер, но наш бот использует polling. Нужно добавить простой HTTP endpoint:

### Создайте файл `render_health.py`:

```python
from aiohttp import web
import asyncio

async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
```

### Обновите `main.py`:

Добавьте в начало файла:
```python
from render_health import start_health_server
```

В функцию `main()` добавьте перед `dp.start_polling`:
```python
# Запуск health check сервера для Render
asyncio.create_task(start_health_server())
```

Я создам эти файлы для вас!

---

## 📊 Мониторинг

### Просмотр логов:
1. В Render Dashboard откройте ваш сервис
2. Перейдите в "Logs"
3. Видите все логи в реальном времени

### Проверка статуса:
- В Dashboard видно: Running / Sleeping / Failed
- Зеленый = работает
- Серый = спит
- Красный = ошибка

---

## 🔄 Обновление бота

### Автоматическое обновление:
1. Внесите изменения в код локально
2. Загрузите на GitHub (commit + push)
3. Render автоматически задеплоит новую версию!

### Ручное обновление:
1. В Render Dashboard нажмите "Manual Deploy"
2. Выберите "Deploy latest commit"

---

## 💰 Лимиты бесплатного плана

### Что входит:
- ✅ 750 часов/месяц (≈25 часов в день)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Автоматический SSL
- ✅ Неограниченный трафик

### Как уложиться в 750 часов:
- **Вариант 1:** Работа 24/7 = 720 часов (уложитесь!)
- **Вариант 2:** С UptimeRobot бот будет просыпаться только при пинге
- **Вариант 3:** Настройте расписание работы

### Что будет после 750 часов:
- Сервис остановится до следующего месяца
- Или перейдите на платный план ($7/мес)

---

## 🎯 Добавление себя в админы

1. **Узнайте свой Telegram ID:**
   - Напишите боту @userinfobot
   - Скопируйте ваш ID (например: 123456789)

2. **Добавьте в Environment Variables:**
   - Вернитесь в Render Dashboard
   - Environment → Add Variable
   - Key: `ADMIN_IDS`
   - Value: `ваш_telegram_id`
   - Save Changes

3. **Render автоматически перезапустит бота**

4. **Проверьте:**
   - Отправьте боту `/admin`
   - Должна открыться админ-панель!

---

## 🐛 Решение проблем

### Бот не запускается:
1. Проверьте логи в Render Dashboard
2. Убедитесь что все переменные окружения добавлены
3. Проверьте что токен правильный

### Бот засыпает:
1. Настройте UptimeRobot (см. выше)
2. Или добавьте health check endpoint

### Ошибка "Application failed to respond":
1. Добавьте `render_health.py` (я создам для вас)
2. Render ожидает HTTP ответ на порту 10000

### База данных не сохраняется:
1. Render использует эфемерное хранилище
2. Для постоянного хранения используйте:
   - PostgreSQL (бесплатно на Render)
   - Или внешнюю БД

---

## 📈 Переход на PostgreSQL (рекомендуется)

### Почему PostgreSQL:
- ✅ Данные не теряются при перезапуске
- ✅ Лучше для production
- ✅ Бесплатно на Render (90 дней, потом $7/мес)

### Как настроить:

1. **Создайте PostgreSQL базу:**
   - В Render Dashboard: New + → PostgreSQL
   - Name: bot-database
   - Plan: Free
   - Create Database

2. **Скопируйте Internal Database URL**

3. **Обновите переменную окружения:**
   ```
   DATABASE_URL = postgresql+asyncpg://user:pass@host/db
   ```
   (используйте Internal Database URL из шага 2)

4. **Render перезапустит бота**

---

## ✅ Чек-лист запуска

- [ ] Создал GitHub репозиторий
- [ ] Загрузил все файлы проекта
- [ ] Зарегистрировался на Render.com
- [ ] Создал Web Service
- [ ] Добавил все переменные окружения
- [ ] Дождался успешного деплоя
- [ ] Проверил логи - "Бот успешно запущен!"
- [ ] Протестировал бота в Telegram
- [ ] Настроил UptimeRobot
- [ ] Добавил себя в админы
- [ ] Проверил админ-панель

---

## 🎉 Готово!

Ваш бот работает на Render.com!

### Следующие шаги:
1. ✅ Протестируйте все функции
2. ✅ Пригласите первых пользователей
3. ✅ Настройте платежные системы (опционально)
4. ✅ Читайте GROWTH_STRATEGY.md для привлечения пользователей

---

## 💡 Советы

### Для стабильной работы:
- Используйте UptimeRobot
- Перейдите на PostgreSQL
- Мониторьте логи первые дни

### Для масштабирования:
- При росте пользователей переходите на платный план ($7/мес)
- Или используйте Oracle Cloud (бесплатно навсегда)

### Для экономии:
- 750 часов хватит на месяц работы 24/7
- Если не хватит - настройте расписание работы

---

## 📞 Поддержка

**Проблемы с Render?**
- Документация: https://render.com/docs
- Поддержка: support@render.com

**Проблемы с ботом?**
- Смотрите FAQ.md
- Проверьте логи
- Создайте issue на GitHub

---

**Удачи с запуском! 🚀**

*P.S. Не забудьте настроить UptimeRobot, чтобы бот не засыпал!*
