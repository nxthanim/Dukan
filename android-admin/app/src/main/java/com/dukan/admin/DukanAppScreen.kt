package com.dukan.admin

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.dukan.admin.screens.ConversationDetailScreen
import com.dukan.admin.screens.ConversationsScreen
import com.dukan.admin.screens.DashboardScreen
import com.dukan.admin.screens.OrdersScreen
import com.dukan.admin.screens.ServicesScreen
import com.dukan.admin.screens.SettingsScreen

@Composable
fun DukanAppScreen() {
    val navController = rememberNavController()
    var serverUrl by remember { mutableStateOf("http://10.0.2.2:8000") }
    
    NavHost(
        navController = navController,
        startDestination = "dashboard"
    ) {
        composable("dashboard") {
            DashboardScreen(
                navController = navController,
                serverUrl = serverUrl,
                onServerUrlChange = { serverUrl = it }
            )
        }
        composable("conversations") {
            ConversationsScreen(
                navController = navController,
                serverUrl = serverUrl
            )
        }
        composable("conversations/{id}") { backStackEntry ->
            val conversationId = backStackEntry.arguments?.getString("id") ?: ""
            ConversationDetailScreen(
                navController = navController,
                conversationId = conversationId,
                serverUrl = serverUrl
            )
        }
        composable("services") {
            ServicesScreen(
                navController = navController,
                serverUrl = serverUrl
            )
        }
        composable("orders") {
            OrdersScreen(
                navController = navController,
                serverUrl = serverUrl
            )
        }
        composable("settings") {
            SettingsScreen(
                navController = navController,
                serverUrl = serverUrl,
                onServerUrlChange = { serverUrl = it }
            )
        }
    }
}
