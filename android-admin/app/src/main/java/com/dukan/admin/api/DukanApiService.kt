package com.dukan.admin.api

import com.dukan.admin.models.*
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

interface DukanApiService {
    
    @GET("conversations")
    suspend fun getConversations(): ConversationsResponse
    
    @GET("conversations/{id}/messages")
    suspend fun getConversationMessages(@Path("id") id: Int): ConversationDetailResponse
    
    @GET("api/services")
    suspend fun getServices(): ServicesResponse
    
    @GET("api/orders")
    suspend fun getOrders(): OrdersResponse
    
    @GET("api/stats")
    suspend fun getStats(): Stats
    
    @POST("api/send-message")
    suspend fun sendMessage(@Body request: SendMessageRequest): ApiResponse<Unit>
    
    @POST("conversations/{id}/flag")
    suspend fun flagConversation(
        @Path("id") id: Int,
        @Body request: Map<String, Boolean>
    ): ApiResponse<Unit>
    
    @GET("health")
    suspend fun healthCheck(): Map<String, String>
}

object DukanApi {
    private const val BASE_URL_VAR = "http://10.0.2.2:8000/"
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    fun create(baseUrl: String = BASE_URL_VAR): DukanApiService {
        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(DukanApiService::class.java)
    }
}
