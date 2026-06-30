package com.dukan.admin.services

import android.app.Notification
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.dukan.admin.MainActivity
import com.dukan.admin.R
import okhttp3.*
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import java.util.concurrent.TimeUnit

class WebSocketService : Service() {
    
    private var webSocket: WebSocket? = null
    private var client: OkHttpClient = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()
    
    private var serverUrl: String = "ws://10.0.2.2:8000/ws"
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onCreate() {
        super.onCreate()
        startForeground()
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        intent?.let {
            serverUrl = it.getStringExtra("SERVER_URL") ?: "ws://10.0.2.2:8000/ws"
        }
        connectWebSocket()
        return START_STICKY
    }
    
    private fun startForeground() {
        val notificationIntent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, notificationIntent, 
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        val notification = NotificationCompat.Builder(this, "dukan_channel")
            .setContentTitle("Dukan Admin")
            .setContentText("Connected to server")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentIntent(pendingIntent)
            .build()
        
        startForeground(1, notification)
    }
    
    private fun connectWebSocket() {
        val request = Request.Builder()
            .url(serverUrl)
            .build()
        
        val listener = object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                super.onOpen(webSocket, response)
                sendBroadcast(Intent("WS_CONNECTED"))
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                super.onMessage(webSocket, text)
                val intent = Intent("WS_MESSAGE").apply {
                    putExtra("message", text)
                }
                sendBroadcast(intent)
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                super.onClosed(webSocket, code, reason)
                sendBroadcast(Intent("WS_DISCONNECTED"))
                // Reconnect after 5 seconds
                Thread.sleep(5000)
                connectWebSocket()
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                super.onFailure(webSocket, t, response)
                sendBroadcast(Intent("WS_ERROR").apply {
                    putExtra("error", t.message)
                })
                // Reconnect after 5 seconds
                Thread.sleep(5000)
                connectWebSocket()
            }
        }
        
        webSocket = client.newWebSocket(request, listener)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        webSocket?.close(1000, "Service destroyed")
    }
    
    fun updateServerUrl(url: String) {
        serverUrl = url.replace("http", "ws") + "/ws"
        webSocket?.close(1000, "URL changed")
        connectWebSocket()
    }
}
