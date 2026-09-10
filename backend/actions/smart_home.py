"""
Smart Home Integration Module - Control devices via Home Assistant
"""

import logging
import aiohttp
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SmartHomeController:
    """Handle smart home device control"""
    
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.session = None
    
    async def init_session(self):
        """Initialize HTTP session"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    async def call_service(self, domain: str, service: str, entity_id: str, data: Dict = None):
        """Call Home Assistant service"""
        try:
            await self.init_session()
            
            url = f"{self.url}/api/services/{domain}/{service}"
            payload = {"entity_id": entity_id}
            if data:
                payload.update(data)
            
            async with self.session.post(url, json=payload) as resp:
                if resp.status == 200:
                    logger.info(f"Service called: {domain}/{service} on {entity_id}")
                    return {"success": True, "message": f"Controlled {entity_id}"}
                else:
                    error = await resp.text()
                    logger.error(f"Service call failed: {error}")
                    return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Smart home action failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def turn_on(self, entity_id: str):
        """Turn on device"""
        return await self.call_service("homeassistant", "turn_on", entity_id)
    
    async def turn_off(self, entity_id: str):
        """Turn off device"""
        return await self.call_service("homeassistant", "turn_off", entity_id)
    
    async def toggle(self, entity_id: str):
        """Toggle device"""
        return await self.call_service("homeassistant", "toggle", entity_id)
    
    async def set_brightness(self, entity_id: str, brightness: int):
        """Set light brightness (0-255)"""
        return await self.call_service(
            "light", "turn_on", entity_id,
            {"brightness": brightness}
        )
    
    async def set_temperature(self, entity_id: str, temperature: float):
        """Set thermostat temperature"""
        return await self.call_service(
            "climate", "set_temperature", entity_id,
            {"temperature": temperature}
        )
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

# Global smart home instance
_smart_home_instance = None

async def get_smart_home_controller(config) -> SmartHomeController:
    """Get or create smart home controller"""
    global _smart_home_instance
    if _smart_home_instance is None:
        _smart_home_instance = SmartHomeController(
            config.home_assistant_url,
            config.home_assistant_token
        )
    return _smart_home_instance

async def execute_smart_home_action(params: dict) -> Dict:
    """Execute smart home action"""
    from config import Config
    
    if not Config.home_assistant_token:
        return {"success": False, "error": "Smart Home not configured"}
    
    controller = await get_smart_home_controller(Config())
    action = params.get("action_type")
    entity_id = params.get("entity_id")
    
    if action == "turn_on":
        return await controller.turn_on(entity_id)
    
    elif action == "turn_off":
        return await controller.turn_off(entity_id)
    
    elif action == "toggle":
        return await controller.toggle(entity_id)
    
    elif action == "set_brightness":
        return await controller.set_brightness(
            entity_id,
            params.get("brightness", 255)
        )
    
    elif action == "set_temperature":
        return await controller.set_temperature(
            entity_id,
            params.get("temperature", 72)
        )
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}
