#!/bin/bash

# Doma API Telegram Bot Setup Script

echo "🤖 Setting up Doma API Telegram Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python/pip installation."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env_example.txt .env
    echo "✅ Created .env file. Please edit it with your bot token."
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your bot token from @BotFather on Telegram"
echo "2. Edit the .env file and add your bot token"
echo "3. Run the bot with: python3 run_bot.py"
echo ""
echo "Or use the npm scripts:"
echo "- npm run bot:setup  (setup environment)"
echo "- npm run bot:run    (run the bot)"
