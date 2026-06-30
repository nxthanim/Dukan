# Dukan Cloud Deployment Guide

Complete step-by-step guide to deploy Dukan to cloud providers.

## 🎯 Quick Comparison

| Provider | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Railway** | ✅ $5/month credit | ⭐⭐⭐⭐⭐ | Beginners |
| **Render** | ✅ Free | ⭐⭐⭐⭐ | Production |
| **Fly.io** | ✅ Free | ⭐⭐⭐ | Full control |
| **Vercel** | ✅ Free | ⭐⭐⭐⭐ | Frontend only |
| **Netlify** | ✅ Free | ⭐⭐⭐⭐ | Frontend only |

**Recommendation**: Use **Railway** for backend + **Netlify** for frontend (both free).

---

## 🚀 Option 1: Railway (Easiest - Recommended)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub
3. Verify email

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your **Dukan** repository
4. Click **"Deploy"**

### Step 3: Configure Environment Variables
After deployment starts, go to **Variables** tab and add:

```
TELEGRAM_BOT_TOKEN=your_bot_token_from_BotFather
CLAUDE_API_KEY=your_claude_api_key
WEBHOOK_URL=$RAILWAY_PUBLIC_DOMAIN/webhook
```

### Step 4: Wait for Deployment
- Railway will automatically:
  - Install dependencies
  - Initialize database
  - Start the server
- This takes **2-5 minutes**

### Step 5: Set Telegram Webhook
```bash
# Replace YOUR_TOKEN and YOUR_DOMAIN
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://YOUR_DOMAIN.up.railway.app/webhook"
```

### Step 6: Deploy Frontend to Netlify
1. Go to https://app.netlify.com
2. Sign up with GitHub
3. Click **"Add new site"** → **"Import from Git"**
4. Select your Dukan repository
5. Set build settings:
   - Build command: `cd react-admin && npm install && npm run build`
   - Publish directory: `react-admin/build`
6. Add environment variable:
   - `REACT_APP_API_URL=https://YOUR_RAILWAY_DOMAIN.up.railway.app`
7. Click **"Deploy site"**

### Step 7: Test
1. Open Telegram and message your bot
2. Open your Netlify frontend URL
3. You should see conversations appearing!

---

## 🌐 Option 2: Render (Free Tier)

### Step 1: Sign Up
1. Go to https://render.com
2. Sign up with GitHub
3. Verify email

### Step 2: Create Backend Service
1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - Name: `dukan-backend`
   - Region: Choose closest
   - Branch: `main`
   - Root Directory: (leave empty)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py --bot`
4. Add Environment Variables:
   ```
   TELEGRAM_BOT_TOKEN=your_token
   CLAUDE_API_KEY=your_key
   WEBHOOK_URL=https://dukan-backend.onrender.com/webhook
   ```
5. Click **"Create Web Service"**

### Step 3: Wait for Deployment (~5-10 minutes)
- Render will build and deploy your backend
- Note your service URL: `https://dukan-backend.onrender.com`

### Step 4: Set Telegram Webhook
```bash
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://dukan-backend.onrender.com/webhook"
```

### Step 5: Deploy Frontend to Netlify
Same as Railway (Step 6 above), but use your Render URL:
- `REACT_APP_API_URL=https://dukan-backend.onrender.com`

---

## ☁️ Option 3: Fly.io (More Control)

### Step 1: Install flyctl
```bash
# Mac/Linux
curl -L https://fly.io/install.sh | sh

# Windows (WSL or Git Bash)
powershell -Command "iwr https://fly.io/install.ps1 -UseBasicParsing | iex"
```

### Step 2: Sign Up
```bash
flyctl auth signup
# Follow the prompts
```

### Step 3: Deploy Backend
```bash
# Navigate to your Dukan directory
cd Dukan

# Create app
flyctl apps create dukan-backend

# Set secrets
flyctl secrets set TELEGRAM_BOT_TOKEN=your_token
flyctl secrets set CLAUDE_API_KEY=your_key

# Deploy
flyctl deploy
```

### Step 4: Set Webhook
```bash
# Get your app URL
flyctl apps list

# Set webhook
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://dukan-backend.fly.dev/webhook"
```

### Step 5: Deploy Frontend to Netlify
Same as above, use: `REACT_APP_API_URL=https://dukan-backend.fly.dev`

---

## 🎨 Option 4: Local with Ngrok (Testing Only)

### Step 1: Install Ngrok
```bash
# Mac/Linux
brew install ngrok/ngrok/ngrok

# Windows
choco install ngrok

# Or download from https://ngrok.com
```

### Step 2: Start Backend
```bash
python main.py --bot
```

### Step 3: Expose with Ngrok
```bash
ngrok http 8000
```

### Step 4: Set Webhook
```bash
# Copy the Forwarding URL from ngrok (e.g., https://abc123.ngrok.io)
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://abc123.ngrok.io/webhook"
```

### Step 5: Start Frontend
```bash
cd react-admin
npm start
```

### Step 6: Access
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Bot: Test on Telegram

**Note**: Ngrok free URLs change every time you restart. For production, use a cloud provider.

---

## 📱 Option 5: Android Admin App

If you want to monitor on your phone:

1. **Deploy backend** to any cloud provider above
2. **Build the APK** from `android-admin/` folder
3. **Install on your phone**
4. **Configure server URL** in the app settings

See [android-admin/BUILD_GUIDE.md](android-admin/BUILD_GUIDE.md) for details.

---

## 🔧 Common Issues & Fixes

### "Webhook not set"
```bash
# Check current webhook
curl "https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo"

# Delete webhook
curl "https://api.telegram.org/botYOUR_TOKEN/deleteWebhook"

# Set webhook again
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=YOUR_URL/webhook"
```

### "Connection refused"
- Make sure your server is running
- Check the port (default: 8000)
- Verify the URL is correct

### "CORS error"
Your backend already has CORS enabled. If you get CORS errors:
- Make sure you're using the correct URL
- Check if your frontend URL is in the allowed origins

### "Database not initialized"
```bash
# Run this once
python main.py --init-db
```

### "Claude API error"
- Verify your API key is correct
- Check your Claude account has credits
- Try a different model in `agent.py`

---

## 📊 Monitoring & Logs

### Railway
1. Go to your project on Railway
2. Click **"Logs"** tab
3. View real-time logs

### Render
1. Go to your service on Render
2. Click **"Logs"** tab
3. View and search logs

### Fly.io
```bash
# View logs
flyctl logs

# Tail logs
flyctl logs --tail
```

---

## 🔒 Security Best Practices

### 1. Use HTTPS
All cloud providers above provide HTTPS by default. Never use HTTP in production.

### 2. Protect Your Tokens
- Never commit `.env` files to Git
- Use environment variables/secrets
- Rotate tokens if compromised

### 3. Rate Limiting
Consider adding rate limiting to your backend to prevent abuse.

### 4. Authentication (Optional)
For the admin dashboard, you can add basic auth:
```python
# In bot.py, add to FastAPI
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "your_password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/api/services")
async def get_services(auth: bool = Depends(verify_credentials)):
    # ... existing code
```

---

## 📈 Scaling

### Vertical Scaling
- Upgrade your plan on Railway/Render
- Use larger instances

### Horizontal Scaling
- Use a load balancer
- Run multiple instances
- Use a database that supports connections from multiple instances

### Database
For production with high traffic, switch from SQLite to PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to cloud provider
- [ ] Frontend deployed to Netlify/Vercel
- [ ] Telegram webhook set
- [ ] Bot responding to messages
- [ ] Admin dashboard showing conversations
- [ ] Real-time updates working
- [ ] All features tested

---

## 💡 Tips

1. **Start with Railway** - It's the easiest and has a generous free tier
2. **Use Netlify for frontend** - Free, fast, and easy
3. **Test locally first** - Make sure everything works before deploying
4. **Monitor logs** - Check for errors regularly
5. **Backup your database** - SQLite file is in your project directory

---

## 📞 Need Help?

1. **Check logs** - Most issues are visible in logs
2. **Verify environment variables** - Most deployment failures are due to missing vars
3. **Test webhook** - Use `curl` to verify webhook is set
4. **Ask for help** - Open a GitHub issue with details

---

**Happy deploying!** 🚀 Your printing business bot will be live in minutes!
