"""
Tools for the Claude agent to use
Three tools: get_price, create_quote, log_order
"""
from typing import Optional, Dict, Any
from database import db
import asyncio


class Tools:
    """Container for all agent tools"""
    
    @staticmethod
    async def get_price(service_name: str) -> Dict[str, Any]:
        """
        Get the price for a service by name
        
        Args:
            service_name: The name of the service to look up
            
        Returns:
            Dict with service details or error message
        """
        service = await db.get_service_by_name(service_name)
        if service:
            return {
                "success": True,
                "service": {
                    "name": service["name"],
                    "price": service["price"],
                    "description": service["description"]
                }
            }
        else:
            return {
                "success": False,
                "error": f"Service '{service_name}' not found in price list"
            }
    
    @staticmethod
    async def create_quote(service_name: str, quantity: int = 1) -> Dict[str, Any]:
        """
        Create a quote for a service
        
        Args:
            service_name: Name of the service
            quantity: Quantity requested
            
        Returns:
            Dict with quote details or error
        """
        # First, get the service
        service = await db.get_service_by_name(service_name)
        if not service:
            return {
                "success": False,
                "error": f"Service '{service_name}' not found"
            }
        
        unit_price = service["price"]
        total_price = unit_price * quantity
        
        # For now, we don't have conversation_id in this context
        # The agent will handle the conversation context separately
        return {
            "success": True,
            "quote": {
                "service_name": service_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "description": service["description"]
            }
        }
    
    @staticmethod
    async def log_order(customer_id: str, service: str, quantity: int, price: float) -> Dict[str, Any]:
        """
        Log an order to the database
        
        Args:
            customer_id: Customer identifier
            service: Service name
            quantity: Quantity ordered
            price: Total price
            
        Returns:
            Dict with success status
        """
        # For now, we'll just log it - conversation_id will be handled by the agent
        # This is a simplified version for MVP
        try:
            # We need conversation_id, but for MVP we'll use a placeholder
            # The agent will provide the actual conversation_id
            print(f"Order logged: {customer_id} ordered {quantity}x {service} at {price}")
            return {
                "success": True,
                "message": f"Order logged: {quantity}x {service} for {customer_id}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Tool definitions for Claude function calling
TOOL_DEFINITIONS = {
    "get_price": {
        "name": "get_price",
        "description": "Get the price and description for a service from the price list",
        "input_schema": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "The name of the service to look up"
                }
            },
            "required": ["service_name"]
        }
    },
    "create_quote": {
        "name": "create_quote",
        "description": "Create a price quote for a service with given quantity",
        "input_schema": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "The name of the service"
                },
                "quantity": {
                    "type": "integer",
                    "description": "The quantity requested",
                    "default": 1,
                    "minimum": 1
                }
            },
            "required": ["service_name"]
        }
    },
    "log_order": {
        "name": "log_order",
        "description": "Log a customer order to the database",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer identifier"
                },
                "service": {
                    "type": "string",
                    "description": "The service name being ordered"
                },
                "quantity": {
                    "type": "integer",
                    "description": "The quantity ordered",
                    "minimum": 1
                },
                "price": {
                    "type": "number",
                    "description": "The total price for the order"
                }
            },
            "required": ["customer_id", "service", "quantity", "price"]
        }
    }
}


# Tool execution mapping
TOOL_EXECUTORS = {
    "get_price": Tools.get_price,
    "create_quote": Tools.create_quote,
    "log_order": Tools.log_order
}
