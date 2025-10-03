@echo off
echo 🤖 Starting Doma API Telegram Bot...
echo 🔑 Using your bot token: 8483648222:AAHK5Qa9xOxGmGlYV3yvCzaaUziq9taNhow
echo.

REM Set the environment variable
set TELEGRAM_BOT_TOKEN=8483648222:AAHK5Qa9xOxGmGlYV3yvCzaaUziq9taNhow

REM Install dependencies
echo 📦 Installing dependencies...
pip install python-telegram-bot==20.7 requests==2.31.0

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run the bot
echo 🚀 Starting bot...
python start_bot.py

pause
