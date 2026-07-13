"""
Keep-alive server for Render
"""
from flask import Flask
import threading
import os
import time

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
