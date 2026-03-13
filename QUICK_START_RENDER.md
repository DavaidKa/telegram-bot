# ⚡ БЫСТРЫЙ СТАРТ: GitHub → Render (10 минут)

## 📋 Краткая инструкция

### ШАГ 1: GitHub (3 минуты)

1. **Откройте:** https://github.com
2. **Нажмите:** "New" (зеленая кнопка)
3. **Название:** `telegram-bot`
4. **Выберите:** Public
5. **Создайте:** "Create repository"
6. **Нажмите:** "uploading an existing file"
7. **Перетащите:** ВСЕ файлы из `C:\Users\lohhh\Desktop\Тг Бот`
8. **Commit:** "Initial commit" → "Commit changes"

✅ **Готово!** Проект на GitHub!

---

### ШАГ 2: Render (5 минут)

1. **Откройте:** https://render.com
2. **Войдите:** через GitHub
3. **Нажмите:** "New +" → "Web Service"
4. **Выберите:** ваш репозиторий `telegram-bot`
5. **Настройте:**
   ```
   Name: telegram-bot
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Plan: Free
   ```
6. **Добавьте переменные** (Environment):
   ```
   BOT_TOKEN = 8742742015:AAFTS2z3y5MSYGvhwBymmGR7h3RAKpsZ5W0
   DATABASE_URL = sqlite+aiosqlite:///data/bot.db
   VIP_PRICE_USD = 2
   REFERRAL_BONUS_DAYS = 3
   FREE_DAILY_LIMIT = 5
   LOG_LEVEL = INFO
   ```
7. **Создайте:** "Create Web Service"
8. **Дождитесь:** деплоя (2-3 минуты)

✅ **Готово!** Бот работает!

---

### ШАГ 3: UptimeRobot (2 минуты)

Чтобы бот не засыпал:

1. **Откройте:** https://uptimerobot.com
2. **Зарегистрируйтесь** (бесплатно)
3. **Нажмите:** "Add New Monitor"
4. **Настройте:**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Telegram Bot
   URL: https://ваш-сервис.onrender.com
   Monitoring Interval: 5 minutes
   ```
5. **Сохраните**

✅ **Готово!** Бот работает 24/7!

---

### ШАГ 4: Проверка (1 минута)

1. **Откройте Telegram**
2. **Найдите вашего бота**
3. **Отправьте:** `/start`
4. **Работает!** 🎉

---

## 🎯 Добавьте себя в админы

1. **Узнайте ID:** напишите @userinfobot
2. **В Render:** Environment → Add Variable
   ```
   ADMIN_IDS = ваш_telegram_id
   ```
3. **Сохраните** → Render перезапустит бота
4. **Проверьте:** `/admin` в боте

---

## 📊 Мониторинг

**Логи в Render:**
- Dashboard → ваш сервис → Logs
- Должно быть: "Бот успешно запущен!"

**Статус:**
- Зеленый = работает ✅
- Серый = спит 😴
- Красный = ошибка ❌

---

## ⚠️ ВАЖНО!

### Проверьте что .env НЕ загрузился на GitHub:
1. Откройте репозиторий на GitHub
2. Убедитесь что файла `.env` НЕТ
3. Должен быть только `.env.example`

### Если .env загрузился:
1. Удалите его на GitHub
2. Смените токен у @BotFather: `/revoke`

---

## 🎉 ВСЁ ГОТОВО!

Ваш бот работает на Render.com!

**Следующие шаги:**
1. ✅ Протестируйте все функции
2. ✅ Пригласите друзей
3. ✅ Читайте GROWTH_STRATEGY.md

---

## 📚 Подробные инструкции:

- **GITHUB_UPLOAD_GUIDE.md** - детальная инструкция по GitHub
- **RENDER_DEPLOY.md** - детальная инструкция по Render
- **FAQ.md** - ответы на вопросы

---

**Удачи! 🚀**
