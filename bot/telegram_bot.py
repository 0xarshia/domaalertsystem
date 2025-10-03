import os
import json
import subprocess
import sys
import requests
import threading
import queue
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
API_KEY = "v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c"
URL = "https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKEN_LISTED&limit=1"
WEBSITE_URL = "http://localhost:5173"

# Store user IDs for broadcasting
user_ids = set()

# Advanced filter configuration
advanced_filter = {
    'min_price': 0,
    'max_price': float('inf'),
    'max_letters': None,
    'domain_extensions': [],
    'keyword': '',
    'seller_address': '',
    'enabled': False
}

# Flask app for API endpoints
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
bot_application = None
message_queue = queue.Queue()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # Add user to the list for broadcasting
    user_id = update.effective_user.id
    user_ids.add(user_id)
    print(f"✅ User {user_id} added to user_ids. Total users: {len(user_ids)}")
    
    keyboard = [
        [InlineKeyboardButton("🚨 Send Alert", callback_data='send_alert')],
        [InlineKeyboardButton("🌐 Get Website Text", callback_data='get_website_text')],
        [InlineKeyboardButton("📢 Broadcast Test", callback_data='broadcast_test')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '🤖 Welcome to Doma API Bot!\n\n'
        'Available commands:\n'
        '• Send Alert - Check API response\n'
        '• Get Website Text - Fetch text from localhost:5173\n'
        '• Broadcast Test - Send test message to all users',
        reply_markup=reply_markup
    )

async def send_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the send alert button click."""
    query = update.callback_query
    await query.answer()
    
    # Show loading message
    await query.edit_message_text("🔄 Processing alert... Please wait...")
    
    try:
        # Run the doma_curl.py script
        result = await run_doma_api()
        
        if result['success']:
            # Extract name and type from response
            extracted_data = extract_name_and_type(result['response'])
            
            message = "✅ Alert sent successfully!\n\n"
            message += f"📊 API Response:\n```json\n{json.dumps(result['response'], indent=2)}\n```\n\n"
            
            if extracted_data:
                message += "📋 Extracted Data:\n"
                for i, item in enumerate(extracted_data, 1):
                    message += f"{i}. Name: `{item.get('name', 'N/A')}`\n"
                    message += f"   Type: `{item.get('type', 'N/A')}`\n\n"
            else:
                message += "⚠️ No name/type data found in response\n"
        else:
            message = f"❌ Error: {result['error']}"
            
    except Exception as e:
        message = f"❌ Unexpected error: {str(e)}"
    
    # Add button to try again
    keyboard = [
        [InlineKeyboardButton("🔄 Try Again", callback_data='send_alert')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def get_website_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the get website text button click."""
    query = update.callback_query
    await query.answer()
    
    # Show loading message
    await query.edit_message_text("🔄 Fetching website content... Please wait...")
    
    try:
        # Fetch content from localhost:5173
        response = requests.get(WEBSITE_URL, timeout=10)
        
        if response.status_code == 200:
            # Extract text content (basic HTML parsing)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text content
            text_content = soup.get_text(separator='\n', strip=True)
            
            # Limit message length (Telegram has message limits)
            if len(text_content) > 3000:
                text_content = text_content[:3000] + "\n\n... (truncated)"
            
            message = "✅ Website content fetched successfully!\n\n"
            message += f"🌐 Content from {WEBSITE_URL}:\n\n"
            message += f"```\n{text_content}\n```"
            
        else:
            message = f"❌ Error fetching website: HTTP {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        message = f"❌ Could not connect to {WEBSITE_URL}\n\nMake sure the website is running on localhost:5173"
    except Exception as e:
        message = f"❌ Error: {str(e)}"
    
    # Add button to try again
    keyboard = [
        [InlineKeyboardButton("🔄 Try Again", callback_data='get_website_text')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def broadcast_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the broadcast test button click."""
    query = update.callback_query
    await query.answer()
    
    if not user_ids:
        await query.edit_message_text("❌ No users to broadcast to. Users need to start the bot first.")
        return
    
    # Show loading message
    await query.edit_message_text("🔄 Broadcasting test message... Please wait...")
    
    success_count = 0
    error_count = 0
    
    for user_id in list(user_ids):  # Create a copy to avoid modification during iteration
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="🧪 Test message from Doma Bot!\n\nThis is a test broadcast to all users who started the bot."
            )
            success_count += 1
        except Exception as e:
            print(f"Error sending to user {user_id}: {e}")
            error_count += 1
            # Remove user from list if they blocked the bot
            if "bot was blocked" in str(e).lower():
                user_ids.discard(user_id)
    
    message = f"📢 Broadcast completed!\n\n"
    message += f"✅ Successfully sent to: {success_count} users\n"
    message += f"❌ Failed to send to: {error_count} users\n"
    message += f"👥 Total users: {len(user_ids)}"
    
    # Add button to try again
    keyboard = [
        [InlineKeyboardButton("🔄 Try Again", callback_data='broadcast_test')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return to main menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🚨 Send Alert", callback_data='send_alert')],
        [InlineKeyboardButton("🌐 Get Website Text", callback_data='get_website_text')],
        [InlineKeyboardButton("📢 Broadcast Test", callback_data='broadcast_test')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        '🤖 Doma API Bot - Main Menu\n\n'
        'Available commands:\n'
        '• Send Alert - Check API response\n'
        '• Get Website Text - Fetch text from localhost:5173\n'
        '• Broadcast Test - Send test message to all users',
        reply_markup=reply_markup
    )

async def run_doma_api():
    """Run the doma API call and return the result."""
    try:
        # Try with requests first (most reliable)
        import requests
        
        headers = {
            'Api-Key': API_KEY
        }
        
        response = requests.get(URL, headers=headers, timeout=1)
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                return {
                    'success': True,
                    'response': json_data
                }
            except json.JSONDecodeError:
                return {
                    'success': True,
                    'response': {'raw_response': response.text}
                }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
            
    except ImportError:
        # Fallback to subprocess curl
        try:
            cmd = [
                'curl',
                URL,
                '--header', f'Api-Key: {API_KEY}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    json_data = json.loads(result.stdout)
                    return {
                        'success': True,
                        'response': json_data
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'response': {'raw_response': result.stdout}
                    }
            else:
                return {
                    'success': False,
                    'error': f"Curl failed: {result.stderr}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': f"Subprocess error: {str(e)}"
            }
    except Exception as e:
        return {
            'success': False,
            'error': f"Request error: {str(e)}"
        }

def extract_name_and_type(response_data):
    """Extract name and type from the API response."""
    extracted = []
    
    def search_recursive(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Look for name and type fields
                if key.lower() == 'name' and isinstance(value, str):
                    extracted.append({
                        'name': value,
                        'type': data.get('type', 'Unknown'),
                        'path': current_path
                    })
                elif key.lower() == 'type' and isinstance(value, str):
                    # Look for corresponding name field
                    name_value = data.get('name', 'Unknown')
                    extracted.append({
                        'name': name_value,
                        'type': value,
                        'path': current_path
                    })
                
                # Recursively search nested objects
                if isinstance(value, (dict, list)):
                    search_recursive(value, current_path)
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                search_recursive(item, f"{path}[{i}]")
    
    search_recursive(response_data)
    return extracted

def find_txhash_deep(obj, path=""):
    """Recursively search for transaction hash in any field that looks like a hash."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this field looks like a transaction hash
            if isinstance(value, str) and len(value) == 66 and value.startswith('0x'):
                print(f"🔍 Found potential txhash at {current_path}: {value}")
                return value
            
            # Recursively search in nested objects
            result = find_txhash_deep(value, current_path)
            if result:
                return result
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            result = find_txhash_deep(item, f"{path}[{i}]")
            if result:
                return result
    
    return None

def find_token_address_deep(obj, path=""):
    """Recursively search for token address in any field that looks like an address."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this field looks like an Ethereum address (42 chars, starts with 0x)
            if isinstance(value, str) and len(value) == 42 and value.startswith('0x'):
                print(f"🔍 Found potential token address at {current_path}: {value}")
                return value
            
            # Recursively search in nested objects
            result = find_token_address_deep(value, current_path)
            if result:
                return result
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            result = find_token_address_deep(item, f"{path}[{i}]")
            if result:
                return result
    
    return None

def find_all_hashes(obj, path=""):
    """Find all potential transaction hashes in the response for debugging."""
    hashes = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this field looks like a transaction hash
            if isinstance(value, str) and len(value) == 66 and value.startswith('0x'):
                hashes.append({
                    'path': current_path,
                    'value': value,
                    'field_name': key
                })
            
            # Recursively search in nested objects
            hashes.extend(find_all_hashes(value, current_path))
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            hashes.extend(find_all_hashes(item, f"{path}[{i}]"))
    
    return hashes

def find_all_addresses(obj, path=""):
    """Find all potential Ethereum addresses in the response for debugging."""
    addresses = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this field looks like an Ethereum address (42 chars, starts with 0x)
            if isinstance(value, str) and len(value) == 42 and value.startswith('0x'):
                addresses.append({
                    'path': current_path,
                    'value': value,
                    'field_name': key
                })
            
            # Recursively search in nested objects
            addresses.extend(find_all_addresses(value, current_path))
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            addresses.extend(find_all_addresses(item, f"{path}[{i}]"))
    
    return addresses

def create_enhanced_message(extracted_data, response_data):
    """Create an enhanced message with properly formatted data and token address link."""
    try:
        # Get basic info
        name = extracted_data.get('name', 'Unknown')
        price = extracted_data.get('price', 0)
        token_address = extracted_data.get('token_address', None)
        
        # Get additional info from response_data
        event_type = 'NAME_TOKEN_LISTED'
        created_at = 'Unknown'
        last_id = 'Unknown'
        
        if 'events' in response_data and len(response_data['events']) > 0:
            event = response_data['events'][0]
            event_type = event.get('type', 'NAME_TOKEN_LISTED')
            if 'eventData' in event and 'eventCreatedAt' in event['eventData']:
                created_at = event['eventData']['eventCreatedAt']
            if 'lastId' in response_data:
                last_id = response_data['lastId']
        
        # Format price (already converted to ETH in extract_data_from_response)
        if price and price > 0:
            formatted_price = f"{price:.6f} ETH"
        else:
            formatted_price = "Price not available"
        
        # Create message
        message = f"🌐 Doma API Data:\n\n"
        message += f"📝 Name: {name}\n"
        message += f"🏷️ Type: {event_type}\n"
        message += f"💰 Price: {formatted_price}\n"
        message += f"📅 Created: {created_at}\n"
        message += f"🆔 LastId: {last_id}\n"
        
        # Add token address link if available
        if token_address:
            message += f"🔗 Token Address: https://explorer-testnet.doma.xyz/address/{token_address}\n"
        else:
            message += f"🔗 Token Address: Not available\n"
        
        return message
        
    except Exception as e:
        print(f"❌ Error creating enhanced message: {e}")
        # Fallback to basic message
        return f"🌐 Doma API Data:\n\n{extracted_data.get('name', 'Unknown')} - Data received but formatting failed"

def extract_data_from_response(response_data):
    """Extract all relevant data from the API response."""
    try:
        extracted_data = {
            'price': None,
            'name': None,
            'seller_address': None,
            'token_address': None
        }
        
        # Check if response has events array
        if 'events' in response_data and isinstance(response_data['events'], list) and len(response_data['events']) > 0:
            event = response_data['events'][0]
            
            print(f"🔍 Extracting data from event: {list(event.keys())}")
            
            # Extract name (domain name)
            if 'name' in event and isinstance(event['name'], str):
                extracted_data['name'] = event['name']
            
            # Comprehensive token address extraction - check multiple possible field names
            token_address_fields = ['tokenAddress', 'token_address', 'address', 'contractAddress', 'contract_address', 'token', 'tokenId', 'token_id']
            for field in token_address_fields:
                if field in event and isinstance(event[field], str) and event[field].strip():
                    extracted_data['token_address'] = event[field].strip()
                    print(f"✅ Found token address in field '{field}': {extracted_data['token_address']}")
                    break
            
            # Extract price from eventData.payment.price
            if 'eventData' in event and isinstance(event['eventData'], dict):
                if 'payment' in event['eventData'] and isinstance(event['eventData']['payment'], dict):
                    if 'price' in event['eventData']['payment']:
                        price = event['eventData']['payment']['price']
                        if isinstance(price, (int, float)):
                            # Convert from wei to ETH (divide by 10^18)
                            extracted_data['price'] = float(price) / 1e18
                        elif isinstance(price, str):
                            try:
                                # Convert from wei to ETH (divide by 10^18)
                                extracted_data['price'] = float(price) / 1e18
                            except ValueError:
                                pass
                
                # Extract seller address
                if 'seller' in event['eventData'] and isinstance(event['eventData']['seller'], str):
                    extracted_data['seller_address'] = event['eventData']['seller']
                elif 'sellerAddress' in event['eventData'] and isinstance(event['eventData']['sellerAddress'], str):
                    extracted_data['seller_address'] = event['eventData']['sellerAddress']
                
                # Extract token address from eventData - comprehensive search
                if not extracted_data['token_address']:  # Only if not found in main event
                    print(f"🔍 Searching eventData for token address: {list(event['eventData'].keys())}")
                    for field in token_address_fields:
                        if field in event['eventData'] and isinstance(event['eventData'][field], str) and event['eventData'][field].strip():
                            extracted_data['token_address'] = event['eventData'][field].strip()
                            print(f"✅ Found token address in eventData['{field}']: {extracted_data['token_address']}")
                            break
            
            # Fallback: look for direct fields in event
            if 'price' in event and isinstance(event['price'], (int, float)):
                # Convert from wei to ETH (divide by 10^18)
                extracted_data['price'] = float(event['price']) / 1e18
            elif 'price' in event and isinstance(event['price'], str):
                try:
                    # Convert from wei to ETH (divide by 10^18)
                    extracted_data['price'] = float(event['price']) / 1e18
                except ValueError:
                    pass
            
            if 'seller' in event and isinstance(event['seller'], str):
                extracted_data['seller_address'] = event['seller']
            elif 'sellerAddress' in event and isinstance(event['sellerAddress'], str):
                extracted_data['seller_address'] = event['sellerAddress']
            
            # Deep search for token address if still not found
            if not extracted_data['token_address']:
                print("🔍 Performing deep search for token address...")
                deep_token_address = find_token_address_deep(event)
                if deep_token_address:
                    extracted_data['token_address'] = deep_token_address
                    print(f"✅ Found token address via deep search: {deep_token_address}")
                else:
                    print("❌ No token address found in any location")
        
        return extracted_data
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {'price': None, 'name': None, 'seller_address': None, 'token_address': None}

def should_send_message(response_data):
    """Check if the message should be sent based on advanced filters."""
    if not advanced_filter['enabled']:
        print("🔍 Filter not enabled, sending message")
        return True
    
    extracted_data = extract_data_from_response(response_data)
    print(f"🔍 Extracted data: {extracted_data}")
    print(f"🔍 Active filters: {advanced_filter}")
    
    # Check price filter
    if advanced_filter['min_price'] > 0 or advanced_filter['max_price'] < float('inf'):
        if extracted_data['price'] is None:
            print("🚫 No price found in response, filtering out message")
            return False
        
        price_in_range = advanced_filter['min_price'] <= extracted_data['price'] <= advanced_filter['max_price']
        print(f"🔍 Price {extracted_data['price']} in range {advanced_filter['min_price']}-{advanced_filter['max_price']}: {price_in_range}")
        if not price_in_range:
            return False
    
    # Check domain name filters
    if extracted_data['name']:
        domain_name = extracted_data['name'].lower()
        
        # Check maximum letters
        if advanced_filter['max_letters'] and len(domain_name) > advanced_filter['max_letters']:
            print(f"🚫 Domain '{domain_name}' has {len(domain_name)} letters, max allowed: {advanced_filter['max_letters']}")
            return False
        
        # Check domain extensions
        if advanced_filter['domain_extensions']:
            # Normalize domain name - remove any leading/trailing whitespace and convert to lowercase
            clean_domain = domain_name.strip().lower()
            
            # Check if domain ends with any of the allowed extensions
            domain_has_extension = any(clean_domain.endswith(ext.lower()) for ext in advanced_filter['domain_extensions'])
            
            print(f"🔍 Domain filtering:")
            print(f"   Raw domain: '{domain_name}'")
            print(f"   Clean domain: '{clean_domain}'")
            print(f"   Allowed extensions: {advanced_filter['domain_extensions']}")
            print(f"   Domain has allowed extension: {domain_has_extension}")
            
            if not domain_has_extension:
                print(f"🚫 Domain '{clean_domain}' does not end with any allowed extension")
                return False
        
        # Check keyword filter
        if advanced_filter['keyword']:
            keyword = advanced_filter['keyword'].lower()
            domain_contains_keyword = keyword in domain_name
            print(f"🔍 Domain '{domain_name}' contains keyword '{keyword}': {domain_contains_keyword}")
            if not domain_contains_keyword:
                return False
    
    # Check seller address filter
    if advanced_filter['seller_address'] and extracted_data['seller_address']:
        seller_match = advanced_filter['seller_address'].lower() in extracted_data['seller_address'].lower()
        print(f"🔍 Seller address '{extracted_data['seller_address']}' matches filter '{advanced_filter['seller_address']}': {seller_match}")
        if not seller_match:
            return False
    
    print("✅ Message passed all filters")
    return True

# Flask API endpoints
@app.route('/api/configure-filter', methods=['POST'])
def configure_filter():
    """API endpoint to configure advanced filters."""
    try:
        data = request.get_json()
        min_price = data.get('minPrice', 0)
        max_price = data.get('maxPrice', float('inf'))
        max_letters = data.get('maxLetters')
        domain_extensions = data.get('domainExtensions', [])
        keyword = data.get('keyword', '')
        seller_address = data.get('sellerAddress', '')
        
        print(f"🔧 Received advanced filter configuration:")
        print(f"   Price: {min_price} - {max_price}")
        print(f"   Max letters: {max_letters}")
        print(f"   Extensions: {domain_extensions}")
        print(f"   Keyword: {keyword}")
        print(f"   Seller: {seller_address}")
        
        global advanced_filter
        advanced_filter = {
            'min_price': min_price,
            'max_price': max_price,
            'max_letters': max_letters,
            'domain_extensions': domain_extensions,
            'keyword': keyword,
            'seller_address': seller_address,
            'enabled': True
        }
        
        print(f"✅ Advanced filters configured")
        print(f"🔧 Current advanced_filter state: {advanced_filter}")
        return jsonify({
            'success': True,
            'message': 'Advanced filters configured successfully'
        })
        
    except Exception as e:
        print(f"❌ Error in configure_filter: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trigger-telegram', methods=['POST'])
def trigger_telegram():
    """API endpoint to trigger telegram broadcast from website."""
    try:
        data = request.get_json()
        message = data.get('message', 'test')
        response_data = data.get('responseData', None)
        
        print(f"🔍 Debug: Received request with message: {message}")
        print(f"🔍 Debug: user_ids count: {len(user_ids)}")
        print(f"🔍 Debug: bot_application: {bot_application is not None}")
        
        if not user_ids:
            print("❌ No users in user_ids set")
            return jsonify({'error': 'No users to send message to. Users need to start the bot first with /start command.'}), 400
        
        if not bot_application:
            print("❌ Bot application not initialized")
            return jsonify({'error': 'Bot not initialized'}), 500
        
        # Check if message should be sent based on price filter
        if response_data:
            print(f"🔍 Checking filter for response data...")
            if not should_send_message(response_data):
                print(f"🚫 Message filtered out due to price filter")
                return jsonify({
                    'success': True,
                    'message': 'Message filtered out due to price range',
                    'filtered': True
                })
            else:
                print(f"✅ Message passed filter, proceeding with broadcast")
                
                # Extract data and create properly formatted message
                extracted_data = extract_data_from_response(response_data)
                print(f"🔍 Extracted data: {extracted_data}")
                
                # Create enhanced message with txhash
                enhanced_message = create_enhanced_message(extracted_data, response_data)
                print(f"🔍 Enhanced message: {enhanced_message}")
                
                # Add enhanced message to queue for the bot to process
                message_queue.put(enhanced_message)
        else:
            print(f"🔍 No response data provided, using original message")
            # Add original message to queue for the bot to process
            message_queue.put(message)
        
        print(f"✅ Broadcast triggered for {len(user_ids)} users")
        return jsonify({
            'success': True,
            'message': f'Broadcast triggered for {len(user_ids)} users'
        })
        
    except Exception as e:
        print(f"❌ Error in trigger_telegram: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-price-extraction', methods=['POST'])
def test_price_extraction():
    """Test endpoint to debug data extraction."""
    try:
        data = request.get_json()
        response_data = data.get('responseData', {})
        
        extracted_data = extract_data_from_response(response_data)
        
        return jsonify({
            'success': True,
            'extracted_data': extracted_data,
            'advanced_filter': advanced_filter,
            'should_send': should_send_message(response_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-api-response', methods=['GET'])
def test_api_response():
    """Test endpoint to see actual API response structure."""
    try:
        import requests
        
        headers = {
            'Api-Key': API_KEY
        }
        
        response = requests.get(URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            extracted_data = extract_data_from_response(data)
            
            # Find all potential addresses in the response
            all_addresses = find_all_addresses(data)
            
            return jsonify({
                'success': True,
                'raw_response': data,
                'extracted_data': extracted_data,
                'domain_name': extracted_data.get('name', 'NOT_FOUND'),
                'domain_length': len(extracted_data.get('name', '')),
                'domain_extensions': [ext for ext in ['.com', '.ai', '.io', '.org', '.net', '.xyz', '.eth'] 
                                    if extracted_data.get('name', '').lower().endswith(ext.lower())],
                'token_address': extracted_data.get('token_address', 'NOT_FOUND'),
                'formatted_price': extracted_data.get('price', 0) / 1e18 if extracted_data.get('price') else 0,
                'all_addresses_found': all_addresses
            })
        else:
            return jsonify({
                'success': False,
                'error': f'API returned status {response.status_code}',
                'response': response.text
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'bot_connected': bot_application is not None,
        'users_count': len(user_ids),
        'advanced_filter': advanced_filter
    })

async def send_broadcast_message(message):
    """Send broadcast message to all users."""
    if not bot_application:
        return
    
    success_count = 0
    error_count = 0
    
    for user_id in list(user_ids):
        try:
            await bot_application.bot.send_message(
                chat_id=user_id,
                text=f"🧪 {message} - Message from website!"
            )
            success_count += 1
        except Exception as e:
            print(f"Error sending to user {user_id}: {e}")
            error_count += 1
            # Remove user from list if they blocked the bot
            if "bot was blocked" in str(e).lower():
                user_ids.discard(user_id)
    
    print(f"Broadcast completed: {success_count} success, {error_count} failed")

def run_flask_app():
    """Run Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=5000, debug=False)

async def process_message_queue():
    """Process messages from the queue."""
    while True:
        try:
            # Check if there are messages in the queue
            if not message_queue.empty():
                message = message_queue.get_nowait()
                await send_broadcast_message(message)
            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
        except queue.Empty:
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error processing message queue: {e}")
            await asyncio.sleep(1)

def main():
    """Start the bot."""
    global bot_application
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set your TELEGRAM_BOT_TOKEN environment variable!")
        print("Get your bot token from @BotFather on Telegram")
        sys.exit(1)
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    bot_application = application  # Set global reference for API
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(send_alert, pattern='^send_alert$'))
    application.add_handler(CallbackQueryHandler(get_website_text, pattern='^get_website_text$'))
    application.add_handler(CallbackQueryHandler(broadcast_test, pattern='^broadcast_test$'))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))
    
    # Add post_init handler to start queue processor
    async def post_init(application):
        asyncio.create_task(process_message_queue())
    
    application.post_init = post_init
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    print("🤖 Bot is starting...")
    print("🌐 API server running on http://localhost:5000")
    print("Press Ctrl+C to stop the bot")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
