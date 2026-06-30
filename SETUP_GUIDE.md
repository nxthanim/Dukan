# Dukan Setup Guide - Quick Reference

## 30-Minute Setup Checklist

### ✅ Step 1: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### ✅ Step 2: Configure Environment (3 min)
```bash
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN and CLAUDE_API_KEY
```

### ✅ Step 3: Create Telegram Bot (5 min)
1. Open Telegram → Search @BotFather
2. Send `/newbot`
3. Name it (e.g., "MyPrintingBot")
4. Copy token to `.env`

### ✅ Step 4: Get Claude API Key (2 min)
1. Go to https://console.anthropic.com/settings/keys
2. Create key
3. Copy to `.env`

### ✅ Step 5: Initialize Database (1 min)
```bash
python main.py --init-db
```

### ✅ Step 6: Start Dukan (1 min)
```bash
python main.py
```

### ✅ Step 7: Test It (5 min)
- Open Telegram → Find your bot
- Send: "What's the price for Business Cards?"
- Send: "I want 50 Flyers"
- Send: "የብሮሽርስ ዋጋ ምን ነው?"

### ✅ Step 8: Monitor (1 min)
- Open http://localhost:8001 in browser
- Or use CLI: `python cli.py list`

## File Structure

```
dukan/
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Full documentation
├── SETUP_GUIDE.md            # This file
├── requirements.txt          # Python dependencies
│
├── config.py                 # Configuration loader
├── database.py               # SQLite database & models
├── tools.py                  # Agent tools (get_price, create_quote, log_order)
├── agent.py                  # Claude AI agent with function calling
├── bot.py                    # Telegram webhook handler
├── main.py                   # Entry point
│
├── cli.py                    # CLI for viewing conversations
├── web_view.py               # Web viewer
└── test_bot.py               # Test script
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `python main.py` | Run bot + web viewer |
| `python main.py --bot` | Run bot only |
| `python main.py --viewer` | Run web viewer only |
| `python main.py --init-db` | Initialize database |
| `python cli.py list` | List all conversations |
| `python cli.py show <id>` | Show conversation details |
| `python cli.py services` | Show price list |
| `python test_bot.py` | Run tests |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | From @BotFather |
| `CLAUDE_API_KEY` | ✅ Yes | From Anthropic console |
| `WEBHOOK_URL` | ❌ No | For production deployment |
| `HOST` | ❌ No | Default: 0.0.0.0 |
| `PORT` | ❌ No | Default: 8000 |
| `DATABASE_URL` | ❌ No | Default: sqlite:///./dukan.db |

## Pre-Seeded Services

| Service | Price (ETB) | Description |
|---------|-------------|-------------|
| Business Cards | 150 | 500 pieces, 350gsm, full color both sides |
| Flyers | 80 | A4, 150gsm, full color single side |
| Posters | 250 | A3, 200gsm glossy, full color |
| Brochures | 200 | A4 tri-fold, 200gsm, full color both sides |
| Banners | 800 | Vinyl, 1m x 2m, full color |
| T-Shirt Printing | 120 | Single color on plain t-shirt |
| Mug Printing | 180 | Full wrap sublimation on mug |
| Stickers | 50 | 100 pieces, vinyl, custom shape |
| Roll-up Banner | 1200 | 85cm x 200cm, aluminum base |
| Letterhead | 100 | A4, 120gsm, company design |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhook` | Telegram webhook |
| GET | `/health` | Health check |
| GET | `/conversations` | List conversations (JSON) |
| GET | `/conversations/{id}/messages` | Get messages |

## Web Viewer

- URL: http://localhost:8001
- Auto-refreshes every 30 seconds
- Shows conversation list with flag status
- Click conversation to see details

## Troubleshooting

**"Module not found"** → Run `pip install -r requirements.txt`

**"Missing environment variables"** → Check `.env` file exists with required keys

**Bot not responding** → Check server is running: `curl http://localhost:8000/health`

**Database errors** → Delete `dukan.db` and re-run `--init-db`

## Deployment Options

### Local Development
```bash
python main.py
```

### Production (VPS)
```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (recommended)
pip install gunicorn
 gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Docker
```bash
# Build
docker build -t dukan .

# Run
docker run -p 8000:8000 --env-file .env dukan
```

## Next Steps

1. ✅ Test with real customers
2. ✅ Monitor conversations in web viewer
3. ✅ Add more services to price list
4. ✅ Customize responses in `agent.py`
5. ✅ Deploy to production

---

**You're ready!** Start your bot and begin serving customers in under 30 minutes. 🚀
