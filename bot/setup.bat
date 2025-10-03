@echo off
REM Doma API Telegram Bot Setup Script for Windows

echo 🤖 Setting up Doma API Telegram Bot...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies. Please check your Python/pip installation.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy env_example.txt .env
    echo ✅ Created .env file. Please edit it with your bot token.
) else (
    echo ✅ .env file already exists.
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Get your bot token from @BotFather on Telegram
echo 2. Edit the .env file and add your bot token
echo 3. Run the bot with: python run_bot.py
echo.
echo Or use the npm scripts:
echo - npm run bot:setup  (setup environment)
echo - npm run bot:run    (run the bot)
echo.
pause
