# Dukan Android Admin App - Build Guide

This is an **admin app for YOUR phone** that connects to your deployed Dukan server. It does NOT run the bot itself - it's for monitoring conversations.

## 📱 What This App Does

- **View all conversations** from your Dukan bot
- **Read and reply** to customer messages
- **Monitor in real-time** with WebSocket updates
- **View services** and orders
- **Get notifications** when human intervention is needed
- **Works offline** (shows cached data)

## ⚠️ Important Understanding

**This is NOT a standalone bot app.** It requires:
1. Your Dukan Python backend running on a server (Render, Railway, VPS, etc.)
2. The server must be accessible from your phone
3. WebSocket connection for real-time updates

```
[Your Phone] → [Android Admin App] → [Your Dukan Server]
                                          ↑
[Telegram] → [Webhook] → [Your Dukan Server] ← [Customers]
```

## 🛠️ Prerequisites

### For Building the APK:
- **Android Studio** (recommended) or just Android SDK
- **Java JDK 17+**
- **Android SDK 34**
- **Gradle 8.4**

### For Running the App:
- **Android 7.0+** (API 24+)
- **Your Dukan server** deployed and running

## 🚀 Build the APK

### Option A: Using Android Studio (Recommended)

1. **Open Android Studio**
2. **File → Open** → Select the `android-admin` folder
3. **Wait for Gradle sync** (this may take a few minutes)
4. **Fix any errors** (Android Studio will guide you)
5. **Build → Build Bundle(s) / APK(s) → Build APK**
6. **APK will be created** at: `android-admin/app/build/outputs/apk/debug/app-debug.apk`

### Option B: Command Line

```bash
# Navigate to android-admin directory
cd android-admin

# Make gradlew executable (if on Linux/Mac)
chmod +x gradlew

# Build debug APK
./gradlew assembleDebug

# APK will be at: app/build/outputs/apk/debug/app-debug.apk
```

### Option C: Build Signed APK (For Release)

1. **Create a keystore** (only once):
```bash
keytool -genkey -v -keystore dukan-release.keystore -alias dukan -keyalg RSA -keysize 2048 -validity 10000
```

2. **Add to app/build.gradle**:
```gradle
android {
    signingConfigs {
        release {
            storeFile file('dukan-release.keystore')
            storePassword 'yourpassword'
            keyAlias 'dukan'
            keyPassword 'yourpassword'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

3. **Build signed APK**:
```bash
./gradlew assembleRelease
```

4. **APK will be at**: `app/build/outputs/apk/release/app-release.apk`

## 📲 Install the APK

### On Your Android Phone:

1. **Transfer the APK** to your phone (email, USB, etc.)
2. **Enable "Unknown Sources"** in Settings → Security
3. **Open the APK file** and install
4. **Open the Dukan Admin app**

### First Run:

1. **Enter your server URL** (e.g., `http://your-server.onrender.com`)
2. **Save** the settings
3. The app will connect and show your dashboard

## 🔧 Configure Server URL

The app needs to connect to your Dukan backend. Set the server URL to:

- **Render**: `https://your-service.onrender.com`
- **Railway**: `https://your-project.up.railway.app`
- **Local testing**: `http://10.0.2.2:8000` (Android emulator) or your local IP
- **Ngrok**: `https://your-ngrok-url.ngrok.io`

**Important**: Make sure your server has CORS enabled for your app.

## 🎨 App Features

### Dashboard
- View total conversations, orders, revenue
- Quick access to all sections
- Real-time updates via WebSocket

### Conversations
- List all conversations
- Filter by status (all, needs human, recent)
- Search conversations
- View full chat history
- Reply to customers

### Services
- View all printing services
- See prices in ETB
- View descriptions in English and Amharic

### Orders
- View all orders
- Search orders
- See total revenue

### Settings
- Change server URL
- Test connection
- View app version

## 🔄 Real-time Updates

The app uses WebSocket to receive real-time updates from your server. When:
- A new message arrives
- A conversation needs human intervention
- Any data changes

The app will automatically refresh the relevant screens.

## ⚡ Performance

- **Offline caching**: Shows cached data when offline
- **Lazy loading**: Loads data as you scroll
- **Efficient API calls**: Minimizes data usage
- **Background sync**: Syncs when connection is restored

## 🐛 Troubleshooting

### "Unable to connect to server"
- Check your server URL is correct
- Make sure your server is running
- Verify your phone has internet connection
- Check if your server has CORS enabled

### "WebSocket connection failed"
- Make sure your server supports WebSocket
- Check if the WebSocket URL is correct (ws:// or wss://)
- Verify no firewall is blocking the connection

### "App crashes on startup"
- Make sure you built the APK correctly
- Check Android version (requires API 24+)
- Look at logcat for error details

### "Data not updating"
- Pull down to refresh manually
- Check WebSocket connection status
- Restart the app

## 📡 API Endpoints Used

The app connects to these endpoints on your server:

- `GET /conversations` - List conversations
- `GET /conversations/{id}/messages` - Get conversation messages
- `GET /api/services` - List services
- `GET /api/orders` - List orders
- `GET /api/stats` - Get dashboard stats
- `POST /api/send-message` - Send message
- `POST /conversations/{id}/flag` - Flag conversation
- `ws://your-server/ws` - WebSocket for real-time updates

## 🔒 Security

- **No data stored** on your phone (except cached data)
- **All data** is fetched from your server
- **HTTPS recommended** for production
- **Authentication** can be added to your server if needed

## 📈 Future Enhancements

- [ ] Push notifications for new messages
- [ ] Biometric authentication
- [ ] Dark mode
- [ ] Multiple server profiles
- [ ] Export data to CSV
- [ ] Charts and analytics

## 🎯 Next Steps

1. ✅ **Build the APK** using Android Studio or command line
2. ✅ **Deploy your Dukan backend** to a cloud server
3. ✅ **Install the APK** on your phone
4. ✅ **Configure the server URL** in the app
5. ✅ **Start monitoring** your printing business!

---

**Need help?** Check the main [README](../README.md) for backend setup instructions.
