"""
Twilio Integration Module - Voice calls and SMS
"""

import logging
from typing import Dict

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

logger = logging.getLogger(__name__)

class TwilioHandler:
    """Handle Twilio SMS and voice calls"""
    
    def __init__(self, account_sid: str, auth_token: str, from_phone: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_phone = from_phone
        
        if TWILIO_AVAILABLE:
            self.client = Client(account_sid, auth_token)
            logger.info("✓ Twilio client initialized")
        else:
            logger.warning("Twilio not available")
            self.client = None
    
    def send_sms(self, to_phone: str, message: str) -> Dict:
        """Send SMS message"""
        try:
            if not self.client:
                return {"success": False, "error": "Twilio not initialized"}
            
            msg = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            
            logger.info(f"SMS sent to {to_phone} (SID: {msg.sid})")
            return {
                "success": True,
                "message_id": msg.sid,
                "to": to_phone
            }
        
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            return {"success": False, "error": str(e)}
    
    def make_call(self, to_phone: str, message: str = None) -> Dict:
        """Make voice call"""
        try:
            if not self.client:
                return {"success": False, "error": "Twilio not initialized"}
            
            # Create TwiML for voice message
            twiml_message = f'<Response><Say>{message or "Hello"}</Say></Response>'
            
            call = self.client.calls.create(
                to=to_phone,
                from_=self.from_phone,
                twiml=twiml_message
            )
            
            logger.info(f"Call initiated to {to_phone} (SID: {call.sid})")
            return {
                "success": True,
                "call_id": call.sid,
                "to": to_phone
            }
        
        except Exception as e:
            logger.error(f"Call failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_call_status(self, call_sid: str) -> Dict:
        """Get call status"""
        try:
            if not self.client:
                return {"success": False, "error": "Twilio not initialized"}
            
            call = self.client.calls(call_sid).fetch()
            return {
                "success": True,
                "status": call.status,
                "duration": call.duration
            }
        
        except Exception as e:
            logger.error(f"Get call status failed: {e}")
            return {"success": False, "error": str(e)}

# Global Twilio instance
_twilio_instance = None

async def get_twilio_handler(config) -> TwilioHandler:
    """Get or create Twilio handler"""
    global _twilio_instance
    if _twilio_instance is None:
        _twilio_instance = TwilioHandler(
            config.twilio_account_sid,
            config.twilio_auth_token,
            config.twilio_phone
        )
    return _twilio_instance

async def execute_twilio_action(params: dict) -> Dict:
    """Execute Twilio action"""
    from config import Config
    
    if not Config.twilio_configured:
        return {"success": False, "error": "Twilio not configured"}
    
    handler = await get_twilio_handler(Config())
    action = params.get("action_type")
    
    if action == "send_sms":
        return handler.send_sms(
            params.get("to_phone"),
            params.get("message")
        )
    
    elif action == "make_call":
        return handler.make_call(
            params.get("to_phone"),
            params.get("message")
        )
    
    elif action == "get_status":
        return handler.get_call_status(params.get("call_sid"))
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}
