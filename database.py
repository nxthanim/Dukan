"""
Database models and operations for Dukan
Uses SQLite for simplicity in MVP
"""
import aiosqlite
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

DATABASE_PATH = "dukan.db"

# Schema for SQLite
INIT_SCHEMA = """
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_chat_id TEXT NOT NULL,
    customer_id TEXT,
    language TEXT DEFAULT 'en',
    needs_human BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    telegram_message_id INTEGER,
    content TEXT NOT NULL,
    is_from_customer BOOLEAN DEFAULT TRUE,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    service_name TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    customer_id TEXT NOT NULL,
    service_name TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE INDEX IF NOT EXISTS idx_conversations_chat_id ON conversations(telegram_chat_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
"""

# Seed data for printing business
SEED_SERVICES = [
    {"name": "Business Cards", "price": 150.0, "description": "500 pieces, 350gsm cardstock, full color both sides"},
    {"name": "Flyers", "price": 80.0, "description": "A4 size, 150gsm paper, full color single side"},
    {"name": "Posters", "price": 250.0, "description": "A3 size, 200gsm glossy paper, full color"},
    {"name": "Brochures", "price": 200.0, "description": "A4 tri-fold, 200gsm paper, full color both sides"},
    {"name": "Banners", "price": 800.0, "description": "Vinyl banner, 1m x 2m, full color"},
    {"name": "T-Shirt Printing", "price": 120.0, "description": "Single color print on plain t-shirt"},
    {"name": "Mug Printing", "price": 180.0, "description": "Full wrap sublimation print on ceramic mug"},
    {"name": "Stickers", "price": 50.0, "description": "100 pieces, vinyl stickers, custom shape"},
    {"name": "Roll-up Banner", "price": 1200.0, "description": "85cm x 200cm, aluminum base, full color print"},
    {"name": "Letterhead", "price": 100.0, "description": "A4 size, 120gsm paper, company letterhead design"},
]

# Amharic translations for seed services
SEED_SERVICES_AMHARIC = [
    {"name": "Business Cards", "amharic_name": "ይለፍ ቃርድ", "price": 150.0, "amharic_description": "500 ንጥል ቃርድ፣ 350gsm ከማንነት ውስጥ፣ ሁለት ጥንቅቅ ቀለም"},
    {"name": "Flyers", "amharic_name": "ፎልደርስ", "price": 80.0, "amharic_description": "A4 መጠን፣ 150gsm ወረቅ፣ አንድ ጥንቅቅ ቀለም"},
    {"name": "Posters", "amharic_name": "ፖስተርስ", "price": 250.0, "amharic_description": "A3 መጠን፣ 200gsm ማለት ወረቅ፣ ሁለት ጥንቅቅ ቀለም"},
    {"name": "Brochures", "amharic_name": "ብሮሽርስ", "price": 200.0, "amharic_description": "A4 ትራይ-ፎልድ፣ 200gsm ወረቅ፣ ሁለት ጥንቅቅ ቀለም"},
    {"name": "Banners", "amharic_name": "ባነርስ", "price": 800.0, "amharic_description": "ቪኒል ባነር፣ 1m x 2m፣ ሁለት ጥንቅቅ ቀለም"},
    {"name": "T-Shirt Printing", "amharic_name": "ቲ-ሻርት ማጽደር", "price": 120.0, "amharic_description": "አንድ ቀለም ማጽደር ላይ ዝግጅት ቲ-ሻርት"},
    {"name": "Mug Printing", "amharic_name": "ኩብ ማጽደር", "price": 180.0, "amharic_description": "ሙሉ ውረት ስብሊሜሽን ማጽደር ላይ ሰርተን ኩብ"},
    {"name": "Stickers", "amharic_name": "ስቲከርስ", "price": 50.0, "amharic_description": "100 ንጥል፣ ቪኒል ስቲከርስ፣ ብቻ ፍጥረት"},
    {"name": "Roll-up Banner", "amharic_name": "ሮል-አፕ ባነር", "price": 1200.0, "amharic_description": "85cm x 200cm፣ አሉሚኒየም ባዘ፣ ሁለት ጥንቅቅ ቀለም"},
    {"name": "Letterhead", "amharic_name": "ደብተር ማንነት", "price": 100.0, "amharic_description": "A4 መጠን፣ 120gsm ወረቅ፣ የኩምፓኒ ደብተር ዘንድ"},
]


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.pool = None
    
    async def initialize(self):
        """Initialize database and seed services"""
        async with aiosqlite.connect(self.db_path) as db:
            # Create tables
            await db.executescript(INIT_SCHEMA)
            await db.commit()
            
            # Check if services are already seeded
            async with db.execute("SELECT COUNT(*) FROM services") as cursor:
                row = await cursor.fetchone()
                if row[0] == 0:
                    # Seed services
                    for service in SEED_SERVICES:
                        await db.execute(
                            "INSERT INTO services (name, price, description) VALUES (?, ?, ?)",
                            (service["name"], service["price"], service["description"])
                        )
                    await db.commit()
    
    async def get_service_by_name(self, name: str) -> Optional[Dict]:
        """Get service by name (case-insensitive)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM services WHERE LOWER(name) = LOWER(?)",
                (name,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
        return None
    
    async def get_all_services(self) -> List[Dict]:
        """Get all services"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM services ORDER BY name") as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_conversation_by_chat_id(self, chat_id: str) -> Optional[Dict]:
        """Get or create conversation by Telegram chat ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            # Check existing
            async with db.execute(
                "SELECT * FROM conversations WHERE telegram_chat_id = ?",
                (chat_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
            
            # Create new
            async with db.execute(
                "INSERT INTO conversations (telegram_chat_id, customer_id, language) VALUES (?, ?, ?)",
                (chat_id, f"customer_{chat_id}", "en")
            ) as cursor:
                await db.commit()
                conv_id = cursor.lastrowid
                return {
                    "id": conv_id,
                    "telegram_chat_id": chat_id,
                    "customer_id": f"customer_{chat_id}",
                    "language": "en",
                    "needs_human": False,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
    
    async def update_conversation_language(self, conversation_id: int, language: str):
        """Update conversation language"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE conversations SET language = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (language, conversation_id)
            )
            await db.commit()
    
    async def flag_conversation_needs_human(self, conversation_id: int, needs_human: bool = True):
        """Flag conversation as needing human intervention"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE conversations SET needs_human = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (needs_human, conversation_id)
            )
            await db.commit()
    
    async def add_message(self, conversation_id: int, content: str, is_from_customer: bool = True, language: str = "en", telegram_message_id: Optional[int] = None):
        """Add a message to conversation"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (conversation_id, telegram_message_id, content, is_from_customer, language) VALUES (?, ?, ?, ?, ?)",
                (conversation_id, telegram_message_id, content, is_from_customer, language)
            )
            await db.commit()
    
    async def create_quote(self, conversation_id: int, service_name: str, quantity: int, unit_price: float, total_price: float):
        """Create a quote"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO quotes (conversation_id, service_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)",
                (conversation_id, service_name, quantity, unit_price, total_price)
            )
            await db.commit()
    
    async def log_order(self, conversation_id: int, customer_id: str, service: str, quantity: int, price: float):
        """Log an order"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO orders (conversation_id, customer_id, service_name, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (conversation_id, customer_id, service, quantity, price)
            )
            await db.commit()
    
    async def get_all_conversations(self) -> List[Dict]:
        """Get all conversations with their flag status"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT id, telegram_chat_id, customer_id, language, needs_human, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        """Get all messages for a conversation"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conversation_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_recent_messages(self, conversation_id: int, limit: int = 10) -> List[Dict]:
        """Get recent messages for context"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?",
                (conversation_id, limit)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in reversed(rows)]


# Global database instance
db = Database()
