"""
Telegram Bot webhook handler for Dukan
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
from database import db
from agent import DukanAgent
from config import Config
import json

app = FastAPI(title="Dukan Telegram Bot")

# Initialize agent
agent = DukanAgent(api_key=Config.CLAUDE_API_KEY)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await db.initialize()
    print("Database initialized")
    
    # Set webhook if WEBHOOK_URL is configured
    if Config.WEBHOOK_URL:
        await set_webhook()


async def set_webhook():
    """Set Telegram webhook"""
    import httpx
    webhook_url = f"{Config.WEBHOOK_URL}/webhook"
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/setWebhook"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"url": webhook_url})
        data = response.json()
        if data.get("ok"):
            print(f"Webhook set to: {webhook_url}")
        else:
            print(f"Failed to set webhook: {data}")


@app.post("/webhook")
async def webhook(request: Request):
    """Handle Telegram webhook updates"""
    try:
        data = await request.json()
        
        # Check if this is a message update
        if "message" in data:
            message = data["message"]
            chat_id = str(message["chat"]["id"])
            text = message.get("text", "")
            message_id = message.get("message_id")
            
            # Ignore commands for now (could add /start later)
            if text.startswith("/"):
                return JSONResponse(content={"status": "ignored"})
            
            # Get or create conversation
            conversation = await db.get_conversation_by_chat_id(chat_id)
            conversation_id = conversation["id"]
            customer_id = conversation["customer_id"]
            language = conversation.get("language", "en")
            
            # Save customer message to database
            await db.add_message(
                conversation_id, text,
                is_from_customer=True,
                language=language,
                telegram_message_id=message_id
            )
            
            # Process message with agent
            response_text, needs_human = await agent.process_message(
                conversation_id, customer_id, text, language
            )
            
            # Send response back to Telegram
            await send_telegram_message(chat_id, response_text)
            
            return JSONResponse(content={"status": "ok", "needs_human": needs_human})
        
        return JSONResponse(content={"status": "ignored"})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def send_telegram_message(chat_id: str, text: str):
    """Send message to Telegram chat"""
    import httpx
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        })
        data = response.json()
        if not data.get("ok"):
            print(f"Failed to send message: {data}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "ok", "version": "1.0.0"})


@app.get("/conversations")
async def list_conversations():
    """List all conversations (for CLI/web viewer)"""
    conversations = await db.get_all_conversations()
    return JSONResponse(content={"conversations": conversations})


@app.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int):
    """Get messages for a conversation"""
    messages = await db.get_conversation_messages(conversation_id)
    return JSONResponse(content={"messages": messages})


def run_server():
    """Run the FastAPI server"""
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )


if __name__ == "__main__":
    run_server()
