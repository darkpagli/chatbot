"""
Keep-alive server for Render
"""
from flask import Flask
import threading
import os
import time
# ==================== ADD THIS AT THE TOP ====================


# Create Flask app for health checks
web_app = Flask(__name__)

@web_app.route('/')
@web_app.route('/health')
def health():
    return "OK", 200

def run_webserver():
    """Start Flask server for health checks"""
    port = int(os.environ.get('PORT', 10000))
    web_app.run(host='0.0.0.0', port=port)

# Start web server in background (non-blocking)
threading.Thread(target=run_webserver, daemon=True).start()
print("🌐 Health check server started on port", os.environ.get('PORT', 10000))

# ==================== YOUR EXISTING BOT CODE BELOW ====================
# (Your bot code continues here...)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Unchitter Bot is running 24/7!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "Pong!", 200

def keep_alive():
    """Start web server"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Start web server in background
threading.Thread(target=keep_alive, daemon=True).start()

print(f"🌐 Web server started on port {os.environ.get('PORT', 8080)}")
print(f"🤖 Bot is running 24/7!")

# Import and start bot
from bot import main

if __name__ == '__main__':
    main()
