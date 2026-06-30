"""
CLI for viewing conversations and their flag status
"""
import asyncio
from database import db
from typing import List, Dict
import argparse
import json


async def list_conversations():
    """List all conversations with their flag status"""
    conversations = await db.get_all_conversations()
    
    if not conversations:
        print("No conversations found")
        return
    
    print("\n" + "=" * 80)
    print("DUKAN CONVERSATIONS")
    print("=" * 80)
    print(f"{'ID':<8} {'Chat ID':<15} {'Customer':<20} {'Language':<10} {'Needs Human':<12} {'Updated'}")
    print("-" * 80)
    
    for conv in conversations:
        needs_human = "✓ YES" if conv["needs_human"] else "✗ NO"
        updated = conv["updated_at"][:19] if conv["updated_at"] else "N/A"
        print(f"{conv['id']:<8} {conv['telegram_chat_id']:<15} {conv['customer_id']:<20} {conv['language']:<10} {needs_human:<12} {updated}")
    
    print("=" * 80)
    print(f"Total: {len(conversations)} conversations")
    needs_human_count = sum(1 for c in conversations if c["needs_human"])
    print(f"Needs Human: {needs_human_count}")
    print()


async def show_conversation(conversation_id: int):
    """Show details of a specific conversation"""
    conversations = await db.get_all_conversations()
    conv = next((c for c in conversations if c["id"] == conversation_id), None)
    
    if not conv:
        print(f"Conversation {conversation_id} not found")
        return
    
    messages = await db.get_conversation_messages(conversation_id)
    
    print("\n" + "=" * 80)
    print(f"CONVERSATION #{conversation_id}")
    print("=" * 80)
    print(f"Chat ID: {conv['telegram_chat_id']}")
    print(f"Customer: {conv['customer_id']}")
    print(f"Language: {conv['language']}")
    print(f"Needs Human: {'YES' if conv['needs_human'] else 'NO'}")
    print(f"Created: {conv['created_at']}")
    print(f"Updated: {conv['updated_at']}")
    print("-" * 80)
    
    if messages:
        print("MESSAGES:")
        for msg in messages:
            role = "CUSTOMER" if msg["is_from_customer"] else "ASSISTANT"
            lang = msg["language"]
            time = msg["created_at"][:19] if msg["created_at"] else "N/A"
            print(f"\n[{time}] {role} ({lang}):")
            print(f"  {msg['content']}")
    else:
        print("No messages in this conversation")
    
    print("=" * 80 + "\n")


async def show_services():
    """Show all services in the price list"""
    services = await db.get_all_services()
    
    print("\n" + "=" * 80)
    print("PRICE LIST")
    print("=" * 80)
    print(f"{'ID':<5} {'Name':<25} {'Price (ETB)':<12} {'Description'}")
    print("-" * 80)
    
    for service in services:
        print(f"{service['id']:<5} {service['name']:<25} {service['price']:<12.2f} {service['description']}")
    
    print("=" * 80)
    print(f"Total: {len(services)} services")
    print()


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Dukan CLI - View conversations and services")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List conversations
    list_parser = subparsers.add_parser("list", help="List all conversations")
    list_parser.set_defaults(func=list_conversations)
    
    # Show conversation
    show_parser = subparsers.add_parser("show", help="Show conversation details")
    show_parser.add_argument("conversation_id", type=int, help="Conversation ID")
    show_parser.set_defaults(func=lambda args: show_conversation(args.conversation_id))
    
    # Show services
    services_parser = subparsers.add_parser("services", help="Show price list")
    services_parser.set_defaults(func=show_services)
    
    args = parser.parse_args()
    
    if not hasattr(args, "func"):
        parser.print_help()
        return
    
    # Initialize database
    await db.initialize()
    
    # Run the command
    await args.func(args)


if __name__ == "__main__":
    asyncio.run(main())
