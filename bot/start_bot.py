#!/usr/bin/env python3
"""
Quick start script for the Telegram bot with your token
"""

import os
import sys
import subprocess

# Set the bot token
os.environ['TELEGRAM_BOT_TOKEN'] = '8483648222:AAHK5Qa9xOxGmGlYV3yvCzaaUziq9taNhow'

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-telegram-bot==20.7', 'requests==2.31.0'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Starting Doma API Telegram Bot...")
    print(f"🔑 Using bot token: {os.environ['TELEGRAM_BOT_TOKEN'][:10]}...")
    
    # Install requirements
    if not install_requirements():
        print("Please install dependencies manually:")
        print("pip install python-telegram-bot==20.7 requests==2.31.0")
        return
    
    # Import and run the bot
    try:
        from telegram_bot import main as bot_main
        print("🚀 Bot is starting...")
        print("Press Ctrl+C to stop the bot")
        bot_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the bot directory and all files are present")
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == '__main__':
    main()
