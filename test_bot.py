"""
Simple test script to verify the bot works locally
"""
import asyncio
from database import db
from agent import DukanAgent
from config import Config


async def test_agent():
    """Test the agent with sample messages"""
    # Initialize database
    await db.initialize()
    
    # Create agent
    agent = DukanAgent(api_key=Config.CLAUDE_API_KEY)
    
    # Create a test conversation
    conv = await db.get_conversation_by_chat_id("test_chat_123")
    conversation_id = conv["id"]
    customer_id = conv["customer_id"]
    
    print("Testing Dukan Agent...")
    print("=" * 60)
    
    # Test messages
    test_messages = [
        "What's the price for Business Cards?",
        "I need 50 Flyers",
        "Can I get a quote for 10 Posters?",
        "Place order for 5 Business Cards",
        "የብሮሽርስ ዋጋ ምን ነው?",
        "What time do you open?",  # Should trigger human
        "I want to book an appointment",  # Should trigger human
    ]
    
    for msg in test_messages:
        print(f"\nCustomer: {msg}")
        response, needs_human = await agent.process_message(
            conversation_id, customer_id, msg, "en"
        )
        flag = " [NEEDS HUMAN]" if needs_human else ""
        print(f"Agent: {response}{flag}")
        print("-" * 60)
    
    print("\nTest complete!")


async def test_database():
    """Test database operations"""
    await db.initialize()
    
    print("Testing Database...")
    print("=" * 60)
    
    # Test services
    services = await db.get_all_services()
    print(f"Services: {len(services)}")
    for s in services[:3]:
        print(f"  - {s['name']}: {s['price']} ETB")
    
    # Test conversation
    conv = await db.get_conversation_by_chat_id("test_chat")
    print(f"\nConversation created: ID={conv['id']}")
    
    # Test messages
    await db.add_message(conv["id"], "Hello!", is_from_customer=True)
    messages = await db.get_conversation_messages(conv["id"])
    print(f"Messages: {len(messages)}")
    
    print("\nDatabase test complete!")


async def main():
    """Run tests"""
    try:
        Config.validate()
    except ValueError as e:
        print(f"Config error: {e}")
        print("Please set TELEGRAM_BOT_TOKEN and CLAUDE_API_KEY in .env")
        return
    
    print("Running Dukan Tests...\n")
    
    await test_database()
    print()
    await test_agent()


if __name__ == "__main__":
    asyncio.run(main())
