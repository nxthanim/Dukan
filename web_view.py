"""
Barebones web viewer for conversations
A simple HTML page that lists conversations and their flag status
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from database import db
from config import Config
import uvicorn

app = FastAPI(title="Dukan Web Viewer")

# HTML template for the web viewer
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dukan - Conversations</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-card .label {
            color: #666;
            font-size: 14px;
        }
        .stat-card .value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .needs-human .value {
            color: #e74c3c;
        }
        .conversation-list {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .conversation-item {
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background 0.2s;
        }
        .conversation-item:hover {
            background: #f9f9f9;
        }
        .conversation-item.needs-human {
            background: #fff5f5;
        }
        .conversation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }
        .chat-id {
            font-weight: bold;
            color: #333;
        }
        .customer-id {
            color: #666;
            font-size: 14px;
        }
        .badges {
            display: flex;
            gap: 10px;
        }
        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .badge-human {
            background: #e74c3c;
            color: white;
        }
        .badge-lang {
            background: #3498db;
            color: white;
        }
        .conversation-preview {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
        .refresh-btn {
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #2980b9;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 Dukan Conversations</h1>
        
        <button class="refresh-btn" onclick="loadConversations()">🔄 Refresh</button>
        
        <div class="stats">
            <div class="stat-card">
                <div class="label">Total Conversations</div>
                <div class="value" id="total-count">0</div>
            </div>
            <div class="stat-card needs-human">
                <div class="label">Needs Human</div>
                <div class="value" id="human-count">0</div>
            </div>
        </div>
        
        <div class="conversation-list" id="conversation-list">
            <div class="loading">Loading conversations...</div>
        </div>
    </div>
    
    <script>
        async function loadConversations() {
            const response = await fetch('/api/conversations');
            const data = await response.json();
            
            const conversations = data.conversations || [];
            const total = conversations.length;
            const needsHuman = conversations.filter(c => c.needs_human).length;
            
            document.getElementById('total-count').textContent = total;
            document.getElementById('human-count').textContent = needsHuman;
            
            const listEl = document.getElementById('conversation-list');
            
            if (conversations.length === 0) {
                listEl.innerHTML = '<div class="loading">No conversations yet</div>';
                return;
            }
            
            let html = '';
            conversations.forEach(conv => {
                const needsHumanClass = conv.needs_human ? 'needs-human' : '';
                const needsHumanBadge = conv.needs_human ? '<span class="badge badge-human">NEEDS HUMAN</span>' : '';
                const langBadge = `<span class="badge badge-lang">${conv.language.toUpperCase()}</span>`;
                
                html += `
                    <div class="conversation-item ${needsHumanClass}" onclick="alert('Chat ID: ${conv.telegram_chat_id}')">
                        <div class="conversation-header">
                            <div>
                                <div class="chat-id">Chat: ${conv.telegram_chat_id}</div>
                                <div class="customer-id">Customer: ${conv.customer_id}</div>
                            </div>
                            <div class="badges">
                                ${langBadge}
                                ${needsHumanBadge}
                            </div>
                        </div>
                        <div class="conversation-preview">
                            Updated: ${new Date(conv.updated_at).toLocaleString()}
                        </div>
                    </div>
                `;
            });
            
            listEl.innerHTML = html;
        }
        
        // Load on page load
        loadConversations();
        
        // Refresh every 30 seconds
        setInterval(loadConversations, 30000);
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def web_viewer():
    """Serve the web viewer HTML"""
    return HTMLResponse(content=HTML_TEMPLATE)


@app.get("/api/conversations")
async def api_conversations():
    """API endpoint for conversations data"""
    conversations = await db.get_all_conversations()
    return JSONResponse(content={"conversations": conversations})


@app.on_event("startup")
async def startup():
    """Initialize database"""
    await db.initialize()


def run_web_viewer():
    """Run the web viewer server"""
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT + 1,  # Run on port 8001 if main is 8000
        reload=True
    )


if __name__ == "__main__":
    run_web_viewer()
