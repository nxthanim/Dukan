# Dukan Deployment Guide

Complete deployment guide for your Dukan Telegram bot with React admin dashboard.

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Telegram Bot Token
- Claude API Key

### Step 1: Clone and Setup
```bash
git clone https://github.com/nxthanim/Dukan.git
cd Dukan
```

### Step 2: Configure Backend
```bash
# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Set these values:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_BotFather
CLAUDE_API_KEY=your_claude_api_key
WEBHOOK_URL=
HOST=0.0.0.0
PORT=8000
```

### Step 3: Initialize Database
```bash
python main.py --init-db
```

### Step 4: Start Backend
```bash
python main.py --bot
```

### Step 5: Start Frontend
```bash
cd react-admin
npm install
npm start
```

### Step 6: Access Admin Dashboard
Open your browser to: http://localhost:3000

---

## 🌐 Production Deployment Options

### Option A: Docker Compose (Recommended)

#### Step 1: Create .env file
```bash
cp .env.example .env
# Edit with your credentials
```

#### Step 2: Build and Run
```bash
docker-compose up -d --build
```

#### Step 3: Access
- **Backend API**: http://localhost:8000
- **Admin Dashboard**: http://localhost:3000

#### Step 4: Set Webhook (for production)
```bash
# Get your server's public IP or domain
# Set WEBHOOK_URL in .env to https://your-domain.com/webhook
# Restart containers
docker-compose down
docker-compose up -d --build
```

### Option B: Separate Servers

#### Backend Server
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python main.py --init-db

# Run with gunicorn (recommended for production)
pip install gunicorn uvicorn
 gunicorn -w 4 -k uvicorn.workers.UvicornWorker bot:app --bind 0.0.0.0:8000
```

#### Frontend Server
```bash
cd react-admin
npm install
npm run build

# Serve with nginx or any static server
# Or use: npx serve -s build -l 3000
```

### Option C: Cloud Deployment (Render, Railway, etc.)

#### Backend (Render Example)
1. Create new Web Service
2. Connect GitHub repository
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `CLAUDE_API_KEY`
   - `WEBHOOK_URL` = https://your-service.onrender.com/webhook
4. Set start command: `python main.py --bot`
5. Deploy

#### Frontend (Vercel/Netlify Example)
1. Create new project
2. Point to `react-admin` directory
3. Set environment variable: `REACT_APP_API_URL` = https://your-backend.onrender.com
4. Deploy

---

## 🔧 Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | From @BotFather |
| `CLAUDE_API_KEY` | ✅ Yes | - | From Anthropic Console |
| `WEBHOOK_URL` | ❌ No | - | For production webhook |
| `HOST` | ❌ No | 0.0.0.0 | Server host |
| `PORT` | ❌ No | 8000 | Server port |
| `DATABASE_URL` | ❌ No | sqlite:///./dukan.db | Database URL |

### React Admin Configuration

Create `react-admin/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_PORT=8000
```

---

## 📡 Telegram Bot Setup

### Create Bot
1. Open Telegram
2. Search for **@BotFather**
3. Send `/newbot`
4. Follow prompts
5. Copy the API token

### Set Webhook (Production)
```bash
# After deploying, set webhook
curl -X POST "https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook?url={YOUR_WEBHOOK_URL}/webhook"
```

### Test Bot
1. Start a chat with your bot
2. Send: "What's the price for Business Cards?"
3. Check admin dashboard for the conversation

---

## 🛠️ Troubleshooting

### Backend Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Missing environment variables"**
```bash
# Check .env file exists
ls -la .env

# Verify variables are set
cat .env
```

**Database errors**
```bash
# Delete and recreate
rm dukan.db
python main.py --init-db
```

### Frontend Issues

**"React scripts not found"**
```bash
cd react-admin
npm install
```

**CORS errors**
```bash
# Make sure backend is running
# Check CORS settings in bot.py
```

### Docker Issues

**"Port already in use"**
```bash
# Stop existing containers
docker-compose down

# Check running containers
docker ps

# Stop specific container
docker stop <container_id>
```

**Build errors**
```bash
# Clean and rebuild
docker-compose down -v
docker-compose up -d --build
```

---

## 📊 Monitoring

### Check Backend Logs
```bash
# Docker
docker logs dukan-backend-1

# Direct
tail -f nohup.out
```

### Check Frontend Logs
```bash
# Docker
docker logs dukan-frontend-1
```

### Database Location
- Local: `./dukan.db`
- Docker: `/app/dukan.db` (inside container)

---

## 🔒 Security

### HTTPS (Required for Webhooks)
Telegram requires HTTPS for webhooks. Options:

1. **Use a reverse proxy** (nginx, Apache) with SSL
2. **Use a cloud provider** with built-in HTTPS (Render, Railway, etc.)
3. **Use ngrok** for local testing with HTTPS

### Example: ngrok for Local Testing
```bash
# Install ngrok
npm install -g ngrok

# Run ngrok
ngrok http 8000

# Set WEBHOOK_URL in .env
WEBHOOK_URL=https://your-ngrok-url.ngrok.io/webhook

# Restart backend
python main.py --bot
```

---

## 📈 Scaling

### Multiple Workers
```bash
# Use gunicorn with multiple workers
gunicorn -w 8 -k uvicorn.workers.UvicornWorker bot:app --bind 0.0.0.0:8000
```

### Database
For production, consider PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dukan
```

---

## 🎯 Next Steps

1. ✅ Deploy backend
2. ✅ Deploy frontend
3. ✅ Set Telegram webhook
4. ✅ Test with real customers
5. ✅ Monitor in admin dashboard
6. ✅ Customize services and responses

---

## 📞 Support

For issues:
- Check logs first
- Verify environment variables
- Test locally before deploying
- Open GitHub issue if needed

---

**Happy deploying!** 🚀
