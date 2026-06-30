"""
Main entry point for Dukan
Runs both the Telegram bot webhook and optionally the web viewer
"""
import argparse
import asyncio
from bot import app as bot_app, run_server as run_bot_server
from web_view import app as web_app, run_web_viewer
from database import db
from config import Config
import uvicorn


def run_bot():
    """Run the Telegram bot server"""
    print("Starting Dukan Telegram Bot...")
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print(f"Webhook URL: {Config.WEBHOOK_URL or 'Not set (use polling)'}")
    run_bot_server()


def run_viewer():
    """Run the web viewer"""
    print("Starting Dukan Web Viewer...")
    print(f"Viewer: http://{Config.HOST}:{Config.PORT + 1}")
    run_web_viewer()


def run_all():
    """Run both bot and viewer concurrently"""
    print("Starting Dukan (Bot + Viewer)...")
    print(f"Bot: http://{Config.HOST}:{Config.PORT}")
    print(f"Viewer: http://{Config.HOST}:{Config.PORT + 1}")
    
    # Run bot in background
    import threading
    bot_thread = threading.Thread(target=run_bot_server, daemon=True)
    bot_thread.start()
    
    # Run viewer in main thread
    run_web_viewer()


async def init_db():
    """Initialize database"""
    await db.initialize()
    print("Database initialized successfully")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Dukan - AI Assistant for Small Business")
    parser.add_argument("--bot", action="store_true", help="Run Telegram bot only")
    parser.add_argument("--viewer", action="store_true", help="Run web viewer only")
    parser.add_argument("--init-db", action="store_true", help="Initialize database and exit")
    
    args = parser.parse_args()
    
    if args.init_db:
        asyncio.run(init_db())
        return
    
    if args.viewer:
        run_viewer()
    elif args.bot:
        run_bot()
    else:
        # Default: run both
        run_all()


if __name__ == "__main__":
    main()
