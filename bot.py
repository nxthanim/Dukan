"""
Telegram Bot webhook handler for Dukan
"""
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Dict, Any, List
from database import db
from agent import DukanAgent
from config import Config
import json
import asyncio

app = FastAPI(title="Dukan Telegram Bot")

# CORS middleware for React admin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = DukanAgent(api_key=Config.CLAUDE_API_KEY)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")

manager = ConnectionManager()


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)


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
            
            # Broadcast update via WebSocket
            await manager.broadcast(json.dumps({
                "type": "NEW_MESSAGE",
                "conversation_id": conversation_id,
                "needs_human": needs_human
            }))
            
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
    """List all conversations (for admin UI)"""
    conversations = await db.get_all_conversations()
    
    # Get last message for each conversation
    conversations_with_last = []
    for conv in conversations:
        messages = await db.get_recent_messages(conv["id"], limit=1)
        last_message = messages[0] if messages else None
        conversations_with_last.append({
            **conv,
            "last_message": last_message
        })
    
    return JSONResponse(content={"conversations": conversations_with_last})


@app.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int):
    """Get messages for a conversation"""
    # Get conversation details
    conversations = await db.get_all_conversations()
    conversation = next((c for c in conversations if c["id"] == conversation_id), None)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await db.get_conversation_messages(conversation_id)
    
    return JSONResponse(content={
        "conversation": conversation,
        "messages": messages
    })


@app.get("/api/services")
async def get_services():
    """Get all services"""
    services = await db.get_all_services()
    return JSONResponse(content={"services": services})


@app.get("/api/orders")
async def get_orders():
    """Get all orders"""
    async with aiosqlite.connect(db.db_path) as db_conn:
        db_conn.row_factory = aiosqlite.Row
        async with db_conn.execute(
            "SELECT * FROM orders ORDER BY created_at DESC"
        ) as cursor:
            rows = await cursor.fetchall()
            orders = [dict(row) for row in rows]
    
    return JSONResponse(content={"orders": orders})


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    conversations = await db.get_all_conversations()
    
    async with aiosqlite.connect(db.db_path) as db_conn:
        db_conn.row_factory = aiosqlite.Row
        
        # Get orders count and total revenue
        async with db_conn.execute(
            "SELECT COUNT(*) as count, SUM(price) as total FROM orders"
        ) as cursor:
            row = await cursor.fetchone()
            orders_count = row["count"] if row else 0
            total_revenue = row["total"] if row and row["total"] else 0
    
    needs_human_count = sum(1 for c in conversations if c["needs_human"])
    
    return JSONResponse(content={
        "totalConversations": len(conversations),
        "needsHuman": needs_human_count,
        "totalOrders": orders_count,
        "totalRevenue": float(total_revenue) if total_revenue else 0
    })


@app.post("/api/send-message")
async def send_message(request: Request):
    """Send a message to a conversation (from admin)"""
    data = await request.json()
    chat_id = data.get("chatId")
    text = data.get("text")
    
    if not chat_id or not text:
        raise HTTPException(status_code=400, detail="chatId and text are required")
    
    # Send via Telegram
    await send_telegram_message(chat_id, text)
    
    # Get conversation
    conversation = await db.get_conversation_by_chat_id(chat_id)
    if conversation:
        # Save as assistant message
        await db.add_message(
            conversation["id"], text,
            is_from_customer=False,
            language=conversation.get("language", "en")
        )
    
    return JSONResponse(content={"status": "ok"})


@app.post("/conversations/{conversation_id}/flag")
async def flag_conversation(conversation_id: int, request: Request):
    """Flag/unflag a conversation as needing human"""
    data = await request.json()
    needs_human = data.get("needsHuman", True)
    
    await db.flag_conversation_needs_human(conversation_id, needs_human)
    
    return JSONResponse(content={"status": "ok", "needsHuman": needs_human})


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
