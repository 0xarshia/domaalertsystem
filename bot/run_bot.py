#!/usr/bin/env python3
"""
Telegram Bot Runner
This script runs the Telegram bot with proper environment setup.
"""

import os
import sys
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def main():
    """Main entry point."""
    print("🤖 Starting Doma API Telegram Bot...")
    
    # Load environment variables
    load_env_file()
    
    # Check if bot token is set
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ Error: TELEGRAM_BOT_TOKEN not found!")
        print("\nTo set up your bot token:")
        print("1. Message @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the bot token")
        print("4. Set it as an environment variable:")
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("   OR create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    # Import and run the bot
    try:
        from telegram_bot import main as bot_main
        bot_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed the requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
