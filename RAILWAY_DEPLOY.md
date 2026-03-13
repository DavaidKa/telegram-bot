# 🚀 Запуск на Railway.app (бесплатно)

## Самый простой способ запустить бота без установки Python!

### Шаг 1: Регистрация (2 минуты)
1. Перейдите на https://railway.app
2. Нажмите "Start a New Project"
3. Войдите через GitHub

### Шаг 2: Загрузка проекта (3 минуты)
1. Создайте репозиторий на GitHub
2. Загрузите туда все файлы проекта
3. В Railway выберите "Deploy from GitHub repo"
4. Выберите ваш репозиторий

### Шаг 3: Настройка переменных (2 минуты)
1. В Railway откройте ваш проект
2. Перейдите в "Variables"
3. Добавьте переменные:
   ```
   BOT_TOKEN=8742742015:AAFTS2z3y5MSYGvhwBymmGR7h3RAKpsZ5W0
   DATABASE_URL=sqlite+aiosqlite:///data/bot.db
   VIP_PRICE_USD=2
   REFERRAL_BONUS_DAYS=3
   FREE_DAILY_LIMIT=5
   LOG_LEVEL=INFO
   ```

### Шаг 4: Деплой (1 минута)
1. Railway автоматически задеплоит проект
2. Подождите 2-3 минуты
3. Проверьте логи - должно быть "Бот успешно запущен!"

### Шаг 5: Проверка
1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте /start
4. Готово! 🎉

---

## Альтернатива: Render.com

1. Перейдите на https://render.com
2. Создайте "New Web Service"
3. Подключите GitHub репозиторий
4. Добавьте переменные окружения
5. Deploy!

---

## Альтернатива: Fly.io

```bash
# Установите Fly CLI
curl -L https://fly.io/install.sh | sh

# Войдите
fly auth login

# Деплой
fly launch
fly secrets set BOT_TOKEN=8742742015:AAFTS2z3y5MSYGvhwBymmGR7h3RAKpsZ5W0
fly deploy
```

---

## ⚠️ Важно!

После запуска на любом хостинге:
1. Узнайте свой Telegram ID: @userinfobot
2. Добавьте его в переменную ADMIN_IDS
3. Перезапустите бота

---

**Бесплатные лимиты:**
- Railway: 500 часов/месяц (достаточно!)
- Render: 750 часов/месяц
- Fly.io: 3 VM бесплатно

Выбирайте любой! 🚀
