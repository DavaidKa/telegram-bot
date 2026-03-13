#!/bin/bash

# Скрипт быстрого старта для Linux/Mac

echo "🚀 Запуск Viral Telegram Bot"
echo "=============================="

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен"
    echo "Установите Python 3.11+ и попробуйте снова"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Проверка .env
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден"
    echo "Создаю из .env.example..."
    cp .env.example .env
    echo "📝 Отредактируйте .env и добавьте BOT_TOKEN"
    echo "Затем запустите скрипт снова"
    exit 1
fi

# Проверка BOT_TOKEN
if ! grep -q "BOT_TOKEN=.*[0-9]" .env; then
    echo "❌ BOT_TOKEN не настроен в .env"
    echo "Получите токен у @BotFather и добавьте в .env"
    exit 1
fi

echo "✅ Конфигурация найдена"

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Создание директорий
mkdir -p data logs

echo ""
echo "✅ Все готово!"
echo ""
echo "🤖 Запуск бота..."
echo "Нажмите Ctrl+C для остановки"
echo ""

# Запуск бота
python main.py
