# 🚀 Быстрый старт за 5 минут

## Шаг 1: Получите токен бота (2 минуты)

1. Откройте Telegram
2. Найдите [@BotFather](https://t.me/BotFather)
3. Отправьте `/newbot`
4. Придумайте имя: `My Viral Bot`
5. Придумайте username: `my_viral_bot`
6. Скопируйте токен (выглядит так: `1234567890:ABCdef...`)

## Шаг 2: Настройте проект (1 минута)

```bash
# Скачайте проект
git clone <your-repo>
cd viral-telegram-bot

# Создайте .env файл
cp .env.example .env

# Откройте .env и вставьте токен
# BOT_TOKEN=ваш_токен_здесь
```

## Шаг 3: Запустите бота (2 минуты)

### Вариант A: Автоматический запуск

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Вариант B: Ручной запуск

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите бота
python main.py
```

### Вариант C: Docker (самый простой)

```bash
docker-compose up -d
```

## Шаг 4: Проверьте работу

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте `/start`
4. Попробуйте создать мем! 🎨

---

## ✅ Готово!

Ваш бот работает! Теперь:

### Следующие шаги:

1. **Добавьте себя в админы**
   ```
   # В .env добавьте свой Telegram ID
   ADMIN_IDS=ваш_telegram_id
   ```
   Узнать ID: [@userinfobot](https://t.me/userinfobot)

2. **Настройте платежи (опционально)**
   - Получите ключи PayPal/YooMoney/QIWI
   - Добавьте в `.env`

3. **Пригласите первых пользователей**
   - Поделитесь ботом с друзьями
   - Добавьте в каталоги ботов
   - Создайте Telegram-канал

4. **Изучите документацию**
   - `README.md` - общая информация
   - `DEPLOYMENT.md` - развертывание на сервере
   - `GROWTH_STRATEGY.md` - как привлечь пользователей
   - `FAQ.md` - ответы на вопросы

---

## 🎯 Основные команды

### Для пользователей:
- `/start` - Главное меню
- `/help` - Справка
- `/stats` - Статистика
- `/referral` - Реферальная ссылка
- `/vip` - Информация о VIP

### Для админов:
- `/admin` - Админ-панель
- `/give_vip user_id days` - Выдать VIP
- `/stats_full` - Полная статистика

---

## 🐛 Что-то не работает?

### Бот не запускается?
```bash
# Проверьте логи
tail -f bot.log

# Или для Docker
docker-compose logs -f bot
```

### Ошибка "Invalid token"?
- Проверьте что токен скопирован полностью
- Убедитесь что нет пробелов в начале/конце
- Токен должен быть в формате: `число:буквы_и_цифры`

### Другие проблемы?
Смотрите `FAQ.md` или создайте issue на GitHub

---

## 📚 Полезные ссылки

- [Документация aiogram](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python.org](https://www.python.org/)
- [Docker документация](https://docs.docker.com/)

---

## 🎉 Поздравляем!

Ваш Telegram-бот готов к работе!

Теперь читайте `GROWTH_STRATEGY.md` чтобы узнать как привлечь пользователей и начать зарабатывать! 💰

---

**Нужна помощь?** Создайте issue на GitHub или напишите в поддержку.

**Понравился проект?** Поставьте ⭐ на GitHub!
