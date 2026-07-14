"""
Webhook server for Render - PERMANENT FIX
"""
from flask import Flask, request, jsonify
import os
import threading
import logging
from telegram import Update
import bot as telegram_bot

# ==================== CONFIG ====================
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# ==================== ROUTES ====================
@app.route('/')
def home():
    return "🤖 Unchitter Bot is running 24/7 with Webhook!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "Pong!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram updates via webhook"""
    try:
        # Get the update data
        data = request.get_json(force=True)
        
        # Create Update object
        update = Update.de_json(data, telegram_bot.create_application().bot)
        
        # Process the update asynchronously
        async def process():
            await telegram_bot.create_application().process_update(update)
        
        # Run in background
        threading.Thread(target=lambda: asyncio.run(process())).start()
        
        return "OK", 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "Error", 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Manually set webhook URL"""
    try:
        webhook_url = os.environ.get('WEBHOOK_URL', 'https://unchitter-bot.onrender.com/webhook')
        import asyncio
        from telegram import Bot
        
        bot = Bot(token=os.environ.get('BOT_TOKEN', '8696983600:AAGUjUJ7KrADo8Xa3--NU7dClihSb70NF3g'))
        result = asyncio.run(bot.set_webhook(webhook_url))
        
        if result:
            return jsonify({"status": "success", "webhook": webhook_url})
        else:
            return jsonify({"status": "error", "message": "Failed to set webhook"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==================== KEEP ALIVE ====================
def keep_alive():
    """Start web server"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Start web server
threading.Thread(target=keep_alive, daemon=True).start()

print("🌐 Webhook server started!")
print(f"📡 Webhook URL: {os.environ.get('WEBHOOK_URL', 'https://unchitter-bot.onrender.com/webhook')}")

# ==================== ASYNC SETUP ====================
import asyncio

async def start_bot():
    """Start the bot in webhook mode"""
    print("🤖 Starting Unchitter Bot in Webhook mode...")
    await telegram_bot.main()

# Start bot
if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped.")
