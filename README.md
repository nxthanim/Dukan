# Dukan - AI Assistant for Small Business

A single-tenant AI assistant that runs a small business's customer chat via Telegram Bot API. This MVP proves the core loop: customers message your Telegram bot, the AI assistant responds with pricing info, creates quotes, and logs orders.

## Features

- **Telegram Bot Webhook**: Receives customer messages via Telegram Bot API
- **Price List**: JSON-based service catalog (Business Cards, Flyers, Posters, etc.)
- **Claude AI Agent**: Uses Claude API with function calling for intelligent responses
- **Three Tools**:
  - `get_price(service_name)` - Get pricing from the catalog
  - `create_quote(service_name, quantity)` - Generate quotes
  - `log_order(customer_id, service, quantity, price)` - Log orders to database
- **Language Detection**: Auto-detects Amharic vs English and responds in the same language
- **Human Handoff**: Flags conversations needing human intervention
- **CLI & Web Viewer**: Simple interfaces to monitor conversations

## Quick Start (Under 30 Minutes)

### Prerequisites

- Python 3.10+
- pip
- Telegram account
- Claude API key

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/nxthanim/Dukan.git
cd Dukan

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

**Required Environment Variables:**

```env
# Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Get from https://console.anthropic.com/settings/keys
CLAUDE_API_KEY=your_claude_api_key_here

# Optional: Set webhook URL for production
WEBHOOK_URL=https://your-domain.com/webhook

# Server settings (optional)
HOST=0.0.0.0
PORT=8000

# Database (SQLite by default)
DATABASE_URL=sqlite:///./dukan.db
```

### Step 3: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow prompts to name your bot (e.g., "Dukan Printing Bot")
4. Copy the **API Token** and paste it into `.env` as `TELEGRAM_BOT_TOKEN`
5. Start a chat with your new bot

### Step 4: Get Claude API Key

1. Go to https://console.anthropic.com/settings/keys
2. Create a new API key
3. Copy and paste into `.env` as `CLAUDE_API_KEY`

### Step 5: Initialize Database

```bash
# Initialize database with seed services
python main.py --init-db
```

This creates `dukan.db` with your printing business services pre-loaded.

### Step 6: Run Dukan

**Option A: Run everything (Bot + Web Viewer)**
```bash
python main.py
```

**Option B: Run bot only**
```bash
python main.py --bot
```

**Option C: Run web viewer only**
```bash
python main.py --viewer
```

### Step 7: Test Your Bot

1. Open Telegram and find your bot
2. Send a message like: "What's the price for Business Cards?"
3. The bot should respond with pricing info
4. Try: "I want 50 Flyers" - should get a quote
5. Try: "Place order for 10 Business Cards" - should log the order
6. Try in Amharic: "የብሮሽርስ ዋጋ ምን ነው?" - should respond in Amharic

### Step 8: Monitor Conversations

**Using CLI:**
```bash
# List all conversations
python cli.py list

# Show specific conversation
python cli.py show 1

# View price list
python cli.py services
```

**Using Web Viewer:**
- Open http://localhost:8001 in your browser
- Shows all conversations with flag status
- Auto-refreshes every 30 seconds

## Project Structure

```
dukan/
├── .env.example           # Environment variables template
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── config.py              # Configuration management
├── database.py            # SQLite database models & operations
├── tools.py               # Agent tools (get_price, create_quote, log_order)
├── agent.py               # Claude AI agent with function calling
├── bot.py                 # Telegram bot webhook handler
├── cli.py                 # CLI for viewing conversations
├── web_view.py            # Barebones web viewer
├── main.py                # Main entry point
└── dukan.db               # SQLite database (created on first run)
```

## Database Schema

### Tables

- **services**: Service catalog (name, price, description)
- **conversations**: Chat sessions (telegram_chat_id, customer_id, language, needs_human)
- **messages**: Chat messages (content, is_from_customer, language)
- **quotes**: Generated quotes (service_name, quantity, prices)
- **orders**: Logged orders (customer_id, service, quantity, price)

### Seed Services

The database is pre-seeded with common printing services:
- Business Cards - 150 ETB
- Flyers - 80 ETB
- Posters - 250 ETB
- Brochures - 200 ETB
- Banners - 800 ETB
- T-Shirt Printing - 120 ETB
- Mug Printing - 180 ETB
- Stickers - 50 ETB
- Roll-up Banner - 1200 ETB
- Letterhead - 100 ETB

## Customization

### Adding Services

Edit `database.py` and add to `SEED_SERVICES` list, then re-run `--init-db`.

### Amharic Support

The agent auto-detects Amharic and responds in Amharic. Translations for services are in `database.py` as `SEED_SERVICES_AMHARIC`.

### Language Detection

The agent uses simple pattern matching for Amharic (Unicode range U+1200 to U+137F). For more accuracy, consider using a language detection library.

## Deployment

### Local Development

Just run `python main.py` - the bot uses polling by default.

### Production (with Webhook)

1. Deploy to a server with HTTPS (e.g., VPS, Render, Railway)
2. Set `WEBHOOK_URL` in `.env` to your server URL
3. Ensure port 8000 is open
4. Run `python main.py --bot`

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py", "--bot"]
```

Build and run:
```bash
docker build -t dukan .
docker run -p 8000:8000 --env-file .env dukan
```

## API Endpoints

- `POST /webhook` - Telegram webhook receiver
- `GET /health` - Health check
- `GET /conversations` - List all conversations (JSON)
- `GET /conversations/{id}/messages` - Get conversation messages

## Web Viewer Endpoints

- `GET /` - HTML viewer
- `GET /api/conversations` - JSON API for conversations

## Troubleshooting

### "Missing required environment variables"

Ensure `.env` file exists with `TELEGRAM_BOT_TOKEN` and `CLAUDE_API_KEY`.

### Bot not responding

1. Check if server is running: `curl http://localhost:8000/health`
2. Verify webhook is set: Check Telegram BotFather for webhook status
3. Check logs for errors

### Claude API errors

1. Verify API key is correct
2. Check your Claude account has credits
3. Try a different model (edit `agent.py`)

### Database issues

Delete `dukan.db` and re-run `--init-db` to reset.

## Roadmap (Future Features)

- [ ] Admin UI for managing services
- [ ] Appointment booking
- [ ] Order history lookup
- [ ] Payment integration
- [ ] Multi-business support
- [ ] Analytics dashboard
- [ ] WhatsApp Cloud API support

## License

MIT License - Feel free to use for your business!

## Support

For issues or questions, open a GitHub issue.

---

**Built for Ethiopian small businesses** 🇪🇹

*Dukan means "shop" in Amharic - a simple, powerful tool for your printing business.*
