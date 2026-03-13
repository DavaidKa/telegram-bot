@echo off
REM Скрипт быстрого старта для Windows

echo 🚀 Запуск Viral Telegram Bot
echo ==============================

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен
    echo Установите Python 3.11+ с python.org
    pause
    exit /b 1
)

echo ✅ Python найден

REM Проверка .env
if not exist .env (
    echo ⚠️  Файл .env не найден
    echo Создаю из .env.example...
    copy .env.example .env
    echo 📝 Отредактируйте .env и добавьте BOT_TOKEN
    echo Затем запустите скрипт снова
    pause
    exit /b 1
)

echo ✅ Конфигурация найдена

REM Создание виртуального окружения
if not exist venv (
    echo 📦 Создание виртуального окружения...
    python -m venv venv
)

REM Активация виртуального окружения
echo 🔧 Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка зависимостей
echo 📥 Установка зависимостей...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Создание директорий
if not exist data mkdir data
if not exist logs mkdir logs

echo.
echo ✅ Все готово!
echo.
echo 🤖 Запуск бота...
echo Нажмите Ctrl+C для остановки
echo.

REM Запуск бота
python main.py

pause
