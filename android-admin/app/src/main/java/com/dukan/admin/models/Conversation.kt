package com.dukan.admin.models

import com.google.gson.annotations.SerializedName

data class Conversation(
    @SerializedName("id") val id: Int,
    @SerializedName("telegram_chat_id") val telegramChatId: String,
    @SerializedName("customer_id") val customerId: String,
    @SerializedName("language") val language: String,
    @SerializedName("needs_human") val needsHuman: Boolean,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("updated_at") val updatedAt: String,
    @SerializedName("last_message") val lastMessage: Message? = null
)

data class Message(
    @SerializedName("id") val id: Int,
    @SerializedName("conversation_id") val conversationId: Int,
    @SerializedName("telegram_message_id") val telegramMessageId: Long?,
    @SerializedName("content") val content: String,
    @SerializedName("is_from_customer") val isFromCustomer: Boolean,
    @SerializedName("language") val language: String,
    @SerializedName("created_at") val createdAt: String
)

data class Service(
    @SerializedName("id") val id: Int,
    @SerializedName("name") val name: String,
    @SerializedName("price") val price: Double,
    @SerializedName("description") val description: String,
    @SerializedName("amharic_name") val amharicName: String?,
    @SerializedName("amharic_description") val amharicDescription: String?
)

data class Order(
    @SerializedName("id") val id: Int,
    @SerializedName("conversation_id") val conversationId: Int,
    @SerializedName("customer_id") val customerId: String,
    @SerializedName("service_name") val serviceName: String,
    @SerializedName("quantity") val quantity: Int,
    @SerializedName("price") val price: Double,
    @SerializedName("created_at") val createdAt: String
)

data class Stats(
    @SerializedName("totalConversations") val totalConversations: Int,
    @SerializedName("needsHuman") val needsHuman: Int,
    @SerializedName("totalOrders") val totalOrders: Int,
    @SerializedName("totalRevenue") val totalRevenue: Double
)

data class ApiResponse<T>(
    @SerializedName("success") val success: Boolean,
    @SerializedName("data") val data: T?,
    @SerializedName("error") val error: String?
)

data class ConversationsResponse(
    @SerializedName("conversations") val conversations: List<Conversation>
)

data class ConversationDetailResponse(
    @SerializedName("conversation") val conversation: Conversation,
    @SerializedName("messages") val messages: List<Message>
)

data class ServicesResponse(
    @SerializedName("services") val services: List<Service>
)

data class OrdersResponse(
    @SerializedName("orders") val orders: List<Order>
)

data class SendMessageRequest(
    val chatId: String,
    val text: String
)

data class WebSocketMessage(
    val type: String,
    val conversationId: Int? = null,
    val needsHuman: Boolean? = null
)
