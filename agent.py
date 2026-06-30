"""
Claude API agent with function calling for Dukan
Handles customer messages, detects language, and uses tools
"""
import anthropic
from typing import Optional, Dict, Any, List, Tuple
from database import db
from tools import TOOL_DEFINITIONS, TOOL_EXECUTORS
import asyncio
import re


class DukanAgent:
    """AI Agent that handles customer conversations"""
    
    # Language detection patterns (simple heuristic for MVP)
    AMHARIC_PATTERNS = [
        r'[\u1200-\u137F]',  # Amharic Unicode range
        r'ሰላም', r'እንደሚና', r'እግዜር', r'ይሁን', r'አማርኛ',
        r'ስለ', r'እንደ', r'ከ', r'ውስጥ', r'ላይ'
    ]
    
    # System prompts for different languages
    SYSTEM_PROMPT_EN = """You are Dukan, a helpful AI assistant for a printing business in Ethiopia.
Your role is to help customers get pricing information, create quotes, and place orders.

You have access to the following tools:
- get_price(service_name): Get price and description for a service
- create_quote(service_name, quantity): Create a quote with quantity
- log_order(customer_id, service, quantity, price): Log an order to the database

IMPORTANT RULES:
1. Always check the price list first before answering pricing questions
2. If a customer asks for something NOT in the price list, reply: "Let me get the owner for you" and flag the conversation
3. If you're unsure about anything, reply: "Let me get the owner for you" and flag the conversation
4. Detect if the customer is writing in Amharic or English and respond in the same language
5. Be concise and helpful
6. For quotes, always show the total price clearly
7. For orders, confirm all details before logging

Available services include: Business Cards, Flyers, Posters, Brochures, Banners, T-Shirt Printing, Mug Printing, Stickers, Roll-up Banner, Letterhead

When you need to flag a conversation for human intervention, use the special response format:
[NEEDS_HUMAN] Let me get the owner for you

Otherwise, respond normally to the customer."""
    
    SYSTEM_PROMPT_AM = """ሮቦት Dukan ነው፣ የኢትዮጵያ ማጽደሪያ ቢዝነስ ለተጠቃሚዎች አሰልጥናቸው።
የእግር አለም አቀራረብ ላይ ለሚገኙ ተጠቃሚዎች የአገልግሎት አሰልጥናቸው ነው።

ለማንኛውም ጉዳይ አሰልጥናቸው አለን።

አቀራረብዎትን ለማግኘት የሚገቡት አሰልጥናት፡
- get_price(አገልግሎት_ስም): የአገልግሎትን ዋጋ እና ማስተካከል ማግኘት
- create_quote(አገልግሎት_ስም, ብዛት): ብዛት ማግኘት
- log_order(ተጠቃሚ_መለያ, አገልግሎት, ብዛት, ዋጋ): ክፍያ ማስቀመጥ

ማስገባት ዋና ሁኔታዎች፡
1. ዋጋ ማጣሪያዎችን ከነገር በፊት አስተካክለን
2. ተጠቃሚው ከዋጋ ማጣሪያዎች ውጭ ነገር አስፈለገው ከሆነ፣ "እግዜሩን አስገብጥናቸው" ብለን አስተካክለን
3. ስለ ነገር አልገባንም፣ "እግዜሩን አስገብጥናቸው" ብለን አስተካክለን
4. ተጠቃሚው ከአማርኛ ወይን ከእንግሊዝኛ ቋንቋ አስተካክለን እና ተጠቃሚውን ቋንቋ ማለገስ
5. አንድነት እና አገልግሎት አሰልጥናቸው
6. ለዋጋ ማጣሪያዎች፣ የአንድ ዋጋን ቅርጽ አሳይ
7. ለክፍያዎች፣ ሁለትን ሁሉ ማረጋገጥ በፊት አስቀምጥ

የሚገኙ አገልግሎቶች፡ ብሮሽርስ፣ ፎልደርስ፣ ፖስተርስ፣ ብሮሽርስ፣ ባነርስ፣ ቲ-ሻርት ማጽደር፣ ኩብ ማጽደር፣ ስቲከርስ፣ ሮል-አፕ ባነር፣ ደብተር ማንነት

ተጠቃሚውን ለእንሰማማት አስፈለገው ከሆነ፣ ይህንን የማስተካከል ቅንብር አስገብጥ፡
[NEEDS_HUMAN] እግዜሩን አስገብጥናቸው

ሌላውን ጊዜ፣ ለተጠቃሚው ቅርጽ አሰልጥናቸው።"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_id = None
        self.customer_id = None
        self.language = "en"
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Amharic or English"""
        for pattern in self.AMHARIC_PATTERNS:
            if re.search(pattern, text):
                return "am"
        return "en"
    
    def get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language"""
        if language == "am":
            return self.SYSTEM_PROMPT_AM
        return self.SYSTEM_PROMPT_EN
    
    async def process_message(self, conversation_id: int, customer_id: str, message: str, chat_language: str = "en") -> Tuple[str, bool]:
        """
        Process a customer message and return response
        
        Args:
            conversation_id: Database conversation ID
            customer_id: Customer identifier
            message: Customer message
            chat_language: Previously detected language for this chat
            
        Returns:
            Tuple of (response_text, needs_human_flag)
        """
        self.conversation_id = conversation_id
        self.customer_id = customer_id
        
        # Detect language from message
        detected_lang = self.detect_language(message)
        self.language = detected_lang
        
        # If chat has a language set, use that as primary
        if chat_language != "en":
            self.language = chat_language
        
        # Update conversation language in DB
        await db.update_conversation_language(conversation_id, self.language)
        
        # Get recent messages for context
        recent_messages = await db.get_recent_messages(conversation_id, limit=5)
        context_messages = []
        for msg in recent_messages:
            role = "user" if msg["is_from_customer"] else "assistant"
            context_messages.append({
                "role": role,
                "content": msg["content"]
            })
        
        # Add current message
        context_messages.append({
            "role": "user",
            "content": message
        })
        
        # Get system prompt
        system_prompt = self.get_system_prompt(self.language)
        
        # Check if message needs human (quick check before API call)
        # This is a simple heuristic - the agent will also flag
        needs_human_quick = self._quick_needs_human_check(message)
        
        try:
            # Call Claude with function calling
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20250620",
                max_tokens=1024,
                temperature=0.7,
                system=system_prompt,
                messages=context_messages,
                tools=TOOL_DEFINITIONS
            )
            
            # Process response
            response_text = ""
            needs_human = False
            
            if response.stop_reason == "tool_use":
                # Handle tool use
                for content in response.content:
                    if isinstance(content, anthropic.ToolUseBlock):
                        tool_name = content.name
                        tool_input = content.input
                        
                        # Execute the tool
                        if tool_name in TOOL_EXECUTORS:
                            executor = TOOL_EXECUTORS[tool_name]
                            tool_result = await executor(**tool_input)
                            
                            # Format tool result for context
                            if tool_name == "get_price":
                                if tool_result.get("success"):
                                    service = tool_result["service"]
                                    if self.language == "am":
                                        response_text = f"ዋጋ፡ {service['price']} ETB\nማስተካከል፡ {service['description']}"
                                    else:
                                        response_text = f"Price: {service['price']} ETB\nDescription: {service['description']}"
                                else:
                                    response_text = tool_result.get("error", "Service not found")
                                    needs_human = True
                            
                            elif tool_name == "create_quote":
                                if tool_result.get("success"):
                                    quote = tool_result["quote"]
                                    if self.language == "am":
                                        response_text = f"ዋጋ ማጣሪያ፡ {quote['service_name']} - {quote['quantity']} ንጥል\nአንድ ዋጋ፡ {quote['unit_price']} ETB\nአጠቃላይ ዋጋ፡ {quote['total_price']} ETB"
                                    else:
                                        response_text = f"Quote for {quote['service_name']} - {quote['quantity']} units\nUnit Price: {quote['unit_price']} ETB\nTotal: {quote['total_price']} ETB"
                                else:
                                    response_text = tool_result.get("error", "Could not create quote")
                                    needs_human = True
                            
                            elif tool_name == "log_order":
                                if tool_result.get("success"):
                                    # Actually log to database
                                    await db.log_order(
                                        conversation_id, customer_id,
                                        tool_input["service"], tool_input["quantity"], tool_input["price"]
                                    )
                                    if self.language == "am":
                                        response_text = f"ክፍያዎ ተረጋግጧል። {tool_input['quantity']}x {tool_input['service']} ከ{tool_input['price']} ETB"
                                    else:
                                        response_text = f"Order confirmed! {tool_input['quantity']}x {tool_input['service']} for {tool_input['price']} ETB"
                                else:
                                    response_text = tool_result.get("error", "Could not log order")
                                    needs_human = True
                        else:
                            response_text = f"Unknown tool: {tool_name}"
                            needs_human = True
                    
                    elif isinstance(content, anthropic.TextBlock):
                        response_text += content.text
            else:
                # Regular text response
                for content in response.content:
                    if isinstance(content, anthropic.TextBlock):
                        response_text += content.text
            
            # Check for NEEDS_HUMAN flag in response
            if "[NEEDS_HUMAN]" in response_text:
                needs_human = True
                response_text = response_text.replace("[NEEDS_HUMAN]", "").strip()
            
            # Also check if response indicates uncertainty
            if needs_human or self._response_needs_human(response_text):
                needs_human = True
                if self.language == "am":
                    if not response_text or "እግዜሩን አስገብጥናቸው" not in response_text:
                        response_text = "እግዜሩን አስገብጥናቸው"
                else:
                    if not response_text or "Let me get the owner for you" not in response_text:
                        response_text = "Let me get the owner for you"
            
            # If we flagged as needs_human, update database
            if needs_human:
                await db.flag_conversation_needs_human(conversation_id, True)
            
            # Save assistant response to database
            await db.add_message(
                conversation_id, response_text, 
                is_from_customer=False, 
                language=self.language
            )
            
            return response_text, needs_human
            
        except Exception as e:
            # Fallback to simple response
            error_msg = f"Error processing message: {str(e)}"
            print(error_msg)
            await db.flag_conversation_needs_human(conversation_id, True)
            await db.add_message(
                conversation_id, error_msg,
                is_from_customer=False,
                language=self.language
            )
            if self.language == "am":
                return "እግዜሩን አስገብጥናቸው", True
            return "Let me get the owner for you", True
    
    def _quick_needs_human_check(self, message: str) -> bool:
        """Quick check if message likely needs human intervention"""
        # Check for appointment booking keywords
        appointment_keywords = [
            "appointment", "book", "schedule", "meeting", "date", "time",
            "ማንኛውን", "ጊዜ", "ሰአት", "ማዘረዘር"
        ]
        
        # Check for order history
        history_keywords = [
            "history", "previous", "past", "order", "status",
            "ታሪክ", "ቀደም", "ክፍያ", "ሁኔታ"
        ]
        
        # Check for custom requests
        custom_keywords = [
            "custom", "special", "unique", "design",
            "ባለት", "ልዩ", "ማስተካከል"
        ]
        
        message_lower = message.lower()
        for kw in appointment_keywords + history_keywords + custom_keywords:
            if kw in message_lower:
                return True
        
        return False
    
    def _response_needs_human(self, response: str) -> bool:
        """Check if agent response indicates need for human"""
        uncertain_patterns = [
            "I'm not sure", "I don't know", "I can't", "I'm unable",
            "አልገባኝም", "አይታወቅንም", "አልቻለኝም"
        ]
        
        response_lower = response.lower()
        for pattern in uncertain_patterns:
            if pattern in response_lower:
                return True
        
        return False
