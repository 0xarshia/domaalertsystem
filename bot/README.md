# Doma API Telegram Bot

A Telegram bot that runs the Doma API curl script and extracts "name" and "type" information from the response.

## Features

- 🤖 Interactive Telegram bot interface
- 🚨 Send Alert button to trigger API calls
- 📊 Displays full API response in formatted JSON
- 🔍 Automatically extracts "name" and "type" fields from response
- 🔄 Retry functionality
- ⚡ Multiple fallback methods (requests, curl, http.client)

## Setup

### 1. Install Dependencies

```bash
cd bot
pip install -r requirements.txt
```

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token you receive

### 3. Configure Bot Token

**Option A: Environment Variable**
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

**Option B: .env File**
```bash
cp env_example.txt .env
# Edit .env and add your bot token
```

### 4. Run the Bot

```bash
python run_bot.py
```

## Usage

1. Start a conversation with your bot on Telegram
2. Send `/start` command
3. Click the "🚨 Send Alert" button
4. The bot will:
   - Run the Doma API call
   - Display the full response
   - Extract and highlight "name" and "type" fields
   - Provide a "Try Again" button for retries

## API Details

The bot calls the Doma API endpoint:
- **URL**: `https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKENIZATION_REQUESTED&limit=1`
- **Method**: GET
- **Headers**: `Api-Key: v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c`

## Response Processing

The bot automatically searches through the API response for:
- Fields named "name" (case-insensitive)
- Fields named "type" (case-insensitive)
- Displays them in a formatted list with their paths

## Troubleshooting

### Bot Token Issues
- Make sure your bot token is correctly set
- Verify the token with @BotFather

### API Connection Issues
- The bot tries multiple methods (requests, curl, http.client)
- Check your internet connection
- Verify the API endpoint is accessible

### Dependencies
- Install all requirements: `pip install -r requirements.txt`
- Make sure Python 3.7+ is installed

## Files

- `telegram_bot.py` - Main bot implementation
- `run_bot.py` - Bot runner with environment setup
- `requirements.txt` - Python dependencies
- `env_example.txt` - Environment configuration template
- `doma_curl.py` - Original API testing script
