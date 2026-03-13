# Инструкция по развертыванию

## Вариант 1: Локальный запуск

### 1. Установка Python 3.11+
```bash
python --version  # Проверка версии
```

### 2. Клонирование и настройка
```bash
git clone <your-repo>
cd viral-telegram-bot
```

### 3. Создание виртуального окружения
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка .env
```bash
cp .env.example .env
# Отредактируйте .env и добавьте BOT_TOKEN
```

### 6. Запуск
```bash
python main.py
```

---

## Вариант 2: Docker (рекомендуется)

### 1. Установка Docker
- Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `curl -fsSL https://get.docker.com | sh`

### 2. Настройка .env
```bash
cp .env.example .env
# Отредактируйте .env
```

### 3. Запуск
```bash
docker-compose up -d
```

### 4. Просмотр логов
```bash
docker-compose logs -f bot
```

### 5. Остановка
```bash
docker-compose down
```

---

## Вариант 3: Бесплатный VPS (Oracle Cloud)

### 1. Создание аккаунта Oracle Cloud
- Перейдите на [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
- Зарегистрируйтесь (бесплатно навсегда)
- Получите 2 VM с 1GB RAM каждая

### 2. Создание VM Instance
```
Shape: VM.Standard.E2.1.Micro (Always Free)
OS: Ubuntu 22.04
```

### 3. Подключение по SSH
```bash
ssh ubuntu@<your-vm-ip>
```

### 4. Установка Docker на сервере
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

### 5. Установка Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 6. Загрузка проекта
```bash
git clone <your-repo>
cd viral-telegram-bot
```

### 7. Настройка .env
```bash
nano .env
# Вставьте ваши данные
```

### 8. Запуск
```bash
docker-compose up -d
```

### 9. Автозапуск при перезагрузке
```bash
sudo systemctl enable docker
```

---

## Вариант 4: Другие бесплатные хостинги

### Railway.app
1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения
4. Deploy автоматически

### Render.com
1. Зарегистрируйтесь на [render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите репозиторий
4. Добавьте переменные окружения

### Fly.io
```bash
# Установка CLI
curl -L https://fly.io/install.sh | sh

# Деплой
fly launch
fly secrets set BOT_TOKEN=your_token
fly deploy
```

---

## Получение BOT_TOKEN

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен и добавьте в `.env`

---

## Настройка платежных систем

### PayPal
1. Зарегистрируйтесь на [developer.paypal.com](https://developer.paypal.com)
2. Создайте приложение
3. Получите Client ID и Secret
4. Добавьте в `.env`

### YooMoney
1. Зарегистрируйтесь на [yoomoney.ru](https://yoomoney.ru)
2. Получите токен API
3. Добавьте в `.env`

### QIWI
1. Зарегистрируйтесь на [qiwi.com](https://qiwi.com)
2. Получите Secret Key
3. Добавьте в `.env`

---

## Мониторинг и обслуживание

### Просмотр логов
```bash
# Docker
docker-compose logs -f bot

# Локально
tail -f bot.log
```

### Обновление бота
```bash
git pull
docker-compose down
docker-compose up -d --build
```

### Резервное копирование БД
```bash
# SQLite
cp data/bot.db data/bot.db.backup

# PostgreSQL
docker-compose exec postgres pg_dump -U botuser botdb > backup.sql
```

---

## Масштабирование

### Переход на PostgreSQL
1. Раскомментируйте секцию postgres в `docker-compose.yml`
2. Измените `DATABASE_URL` в `.env`:
```
DATABASE_URL=postgresql+asyncpg://botuser:botpassword@postgres:5432/botdb
```
3. Перезапустите: `docker-compose up -d`

### Добавление Redis для кэширования
```yaml
# В docker-compose.yml
redis:
  image: redis:7-alpine
  restart: unless-stopped
```

### Несколько инстансов бота
```bash
docker-compose up -d --scale bot=3
```

---

## Решение проблем

### Бот не запускается
- Проверьте BOT_TOKEN в .env
- Проверьте логи: `docker-compose logs bot`
- Убедитесь что порты не заняты

### База данных не создается
- Проверьте права на папку data/
- Убедитесь что DATABASE_URL правильный

### Рассылка не работает
- Проверьте настройки планировщика
- Убедитесь что бот запущен 24/7

---

## Безопасность

1. Никогда не коммитьте .env в Git
2. Используйте сильные пароли для БД
3. Регулярно обновляйте зависимости
4. Настройте firewall на сервере
5. Используйте HTTPS для webhook (если используете)

---

## Поддержка

Если возникли проблемы:
1. Проверьте логи
2. Убедитесь что все зависимости установлены
3. Проверьте версию Python (3.11+)
4. Создайте issue в репозитории
