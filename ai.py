"""
Unchitter Bot - Telegram AI Assistant
Developer: @vikash1178
"""

import logging
import requests
import time
import asyncio
import json
import re
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ==================== CONFIG ====================
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
API_URL = os.getenv('API_URL', 'https://wormgpt.freeapihub.workers.dev/chat?q=')

# ==================== LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== COOLDOWN ====================
user_cooldown = {}
user_stats = {}

# ==================== API CALL ====================
def call_api(query):
    """Call API and extract reply text"""
    try:
        response = requests.get(f"{API_URL}{query}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict):
                reply = data.get('reply', data.get('answer', data.get('response', data.get('result', ''))))
                
                if isinstance(reply, dict):
                    reply = reply.get('text', reply.get('message', str(reply)))
                
                if not reply:
                    reply = str(data)
                
                reply = str(reply)
                
                # Clean up wrapper text
                patterns = [
                    r"\{.*?'reply':\s*'",
                    r"\{.*?'answer':\s*'",
                    r"\{.*?'response':\s*'",
                    r"\{.*?'result':\s*'",
                    r"'\s*\}",
                    r'^\{.*?"reply":\s*"',
                    r'^\{.*?"answer":\s*"',
                    r'^\{.*?"response":\s*"',
                    r'^\{.*?"result":\s*"',
                    r'"\s*\}$',
                ]
                
                for pattern in patterns:
                    reply = re.sub(pattern, '', reply)
                
                reply = re.sub(r",?\s*'question':\s*'[^']*'", '', reply)
                reply = re.sub(r",?\s*'status':\s*'[^']*'", '', reply)
                reply = re.sub(r",?\s*\"question\":\s*\"[^\"]*\"", '', reply)
                reply = re.sub(r",?\s*\"status\":\s*\"[^\"]*\"", '', reply)
                
                reply = reply.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
                
                reply = reply.strip()
                if reply.startswith(','):
                    reply = reply[1:].strip()
                if reply.endswith(','):
                    reply = reply[:-1].strip()
                
                return reply.strip()
            
            return str(data)
        else:
            return f"⚠️ API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏰ API Timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return "🔌 Connection Error. Check API."
    except json.JSONDecodeError:
        return "📝 Raw Response: " + response.text[:200]
    except Exception as e:
        return f"❌ Error: {str(e)[:100]}"

# ==================== UI HELPERS ====================
def get_user_stats(user_id):
    """Get user statistics"""
    if user_id not in user_stats:
        user_stats[user_id] = {
            'questions': 0,
            'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    return user_stats[user_id]

def create_main_menu():
    """Create main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data='stats'),
         InlineKeyboardButton("🔄 Clear", callback_data='clear')],
        [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/vikash1178'),
         InlineKeyboardButton("📢 Channel", url='https://t.me/vikash1178')],
        [InlineKeyboardButton("❓ Help", callback_data='help'),
         InlineKeyboardButton("ℹ️ About", callback_data='about')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== COMMANDS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    user = update.effective_user
    stats = get_user_stats(user.id)
    
    welcome = f"""
╔═══════════════════════════════╗
║     🤖 UNCHITTER BOT         ║
╠═══════════════════════════════╣
║                               ║
║  👤 User: {user.first_name}
║  🔧 Dev: @vikash1178
║  📊 Qs: {stats['questions']}
║  📅 First: {stats['first_seen']}
║                               ║
║  🤖 AI Powered Assistant     ║
║  🚀 Fast API responses       ║
║  💡 24/7 Available           ║
║                               ║
╚═══════════════════════════════╝

📌 Commands:
/start - Main Menu
/help - Help Guide
/about - About Bot
/status - API Status
/ping - Latency Check
/stats - Your Stats
/clear - Clear Session

💬 Just type your question!
    """
    
    await update.message.reply_text(welcome, reply_markup=create_main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help guide"""
    help_text = """
╔═══════════════════════════════╗
║     📖 HELP GUIDE             ║
╠═══════════════════════════════╣
║                               ║
║  🤖 What I do:               ║
║  Answer questions using AI   ║
║  Powered by @vikash1178      ║
║                               ║
║  💬 How to use:              ║
║  1. Type your question       ║
║  2. Wait for API response    ║
║  3. Get instant answer       ║
║                               ║
║  📋 Examples:                ║
║  • What is AI?               ║
║  • Write Python code         ║
║  • Explain quantum physics   ║
║                               ║
║  ⚡ Commands:                ║
║  /start - Main Menu          ║
║  /help - This Guide          ║
║  /about - About Bot          ║
║  /status - API Health        ║
║  /ping - Latency Check       ║
║  /stats - Your Stats         ║
║  /clear - Clear Session      ║
║                               ║
╚═══════════════════════════════╝
    """
    await update.message.reply_text(help_text, reply_markup=create_main_menu())

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About bot"""
    about_text = """
╔═══════════════════════════════╗
║     🤖 UNCHITTER BOT         ║
╠═══════════════════════════════╣
║                               ║
║  📱 Telegram Bot              ║
║  👨‍💻 Developer: @vikash1178   ║
║  📦 Version: 6.0.0            ║
║  ⚙️ Engine: Custom API        ║
║  🌐 Host: Render Cloud        ║
║                               ║
║  ✨ Features:                ║
║  ✅ Unlimited Questions      ║
║  ✅ Fast Responses           ║
║  ✅ 24/7 Available           ║
║  ✅ Rate Limiting            ║
║  ✅ User Statistics          ║
║  ✅ Auto-Restart             ║
║                               ║
║  📢 Contact:                 ║
║  @vikash1178                 ║
║                               ║
║  🖤 Built with Passion       ║
║  ⚡ Powered by Code          ║
║                               ║
╚═══════════════════════════════╝
    """
    await update.message.reply_text(about_text, reply_markup=create_main_menu())

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """API status"""
    msg = await update.message.reply_text("⏳ Checking API...")
    
    try:
        start_time = time.time()
        response = requests.get(API_URL, timeout=5)
        latency = round((time.time() - start_time) * 1000, 2)
        
        if response.status_code == 200:
            status_text = f"""
╔═══════════════════════════════╗
║     📡 API STATUS            ║
╠═══════════════════════════════╣
║                               ║
║  ✅ Status: ONLINE            ║
║  🟢 All Systems Operational  ║
║  ⚡ Latency: {latency}ms      ║
║  📡 Endpoint: Active         ║
║                               ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  👨‍💻 @vikash1178             ║
║                               ║
╚═══════════════════════════════╝
            """
            await msg.edit_text(status_text)
        else:
            await msg.edit_text(f"⚠️ API Status: {response.status_code}\nContact @vikash1178")
    except:
        await msg.edit_text("❌ API OFFLINE\nCannot reach API server.\nContact @vikash1178")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping command"""
    start_time = time.time()
    await update.message.reply_text("🏓 Pong!")
    latency = round((time.time() - start_time) * 1000, 2)
    
    ping_text = f"""
╔═══════════════════════════════╗
║     ⚡ LATENCY CHECK         ║
╠═══════════════════════════════╣
║                               ║
║  🏓 Response Time: {latency}ms
║  📶 Status: {'Excellent' if latency < 200 else 'Good' if latency < 500 else 'Slow'}
║                               ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  🤖 Bot is responsive!       ║
║                               ║
╚═══════════════════════════════╝
    """
    await update.message.reply_text(ping_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User statistics"""
    user = update.effective_user
    stats = get_user_stats(user.id)
    
    stats_text = f"""
╔═══════════════════════════════╗
║     📊 YOUR STATS           ║
╠═══════════════════════════════╣
║                               ║
║  👤 User: {user.first_name}
║  📝 Total Questions: {stats['questions']}
║  📅 First Seen: {stats['first_seen']}
║  🕐 Last Activity: {datetime.now().strftime('%H:%M')}
║                               ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  📈 Keep asking questions!   ║
║                               ║
╚═══════════════════════════════╝
    """
    await update.message.reply_text(stats_text)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear session"""
    user_id = update.effective_user.id
    if user_id in user_cooldown:
        del user_cooldown[user_id]
    
    await update.message.reply_text(
        "🧹 Session Cleared!\n"
        "✨ Your session has been reset.\n"
        "💬 Ask something new!"
    )

# ==================== MESSAGE HANDLER ====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user messages"""
    user = update.effective_user
    user_id = user.id
    user_message = update.message.text
    
    stats = get_user_stats(user_id)
    stats['questions'] += 1
    
    current_time = time.time()
    if user_id in user_cooldown:
        if current_time - user_cooldown[user_id] < 2:
            await update.message.reply_text("⏳ Slow down! Please wait 2 seconds between messages.")
            return
    user_cooldown[user_id] = current_time
    
    await update.message.chat.send_action(action="typing")
    answer = call_api(user_message)
    await update.message.reply_text(answer)

# ==================== CALLBACK HANDLER ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'stats':
        await stats(update, context)
    elif query.data == 'clear':
        await clear(update, context)
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'about':
        await about(update, context)
    
    await query.message.edit_reply_markup(reply_markup=None)

# ==================== MAIN ====================
async def main():
    """Start the bot"""
    print("╔═══════════════════════════════╗")
    print("║     🤖 UNCHITTER BOT         ║")
    print("╠═══════════════════════════════╣")
    print("║  👨‍💻 Developer: @vikash1178   ║")
    print("║  📦 Version: 6.0.0            ║")
    print("║  🤖 Status: Starting...       ║")
    print("╚═══════════════════════════════╝")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")
