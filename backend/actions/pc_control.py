"""
PC Control Module - Automate mouse, keyboard, windows, applications
"""

import pyautogui
import logging
import time
import subprocess
import platform

logger = logging.getLogger(__name__)

# Disable pyautogui safety pause between actions (for speed)
pyautogui.PAUSE = 0.1

class PCController:
    """Handle PC automation and control"""
    
    @staticmethod
    def move_mouse(x: int, y: int, duration: float = 1.0):
        """Move mouse to position"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            logger.info(f"Moved mouse to ({x}, {y})")
            return {"success": True, "message": f"Mouse moved to ({x}, {y})"}
        except Exception as e:
            logger.error(f"Mouse move failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def click(x: int = None, y: int = None, button: str = 'left', clicks: int = 1):
        """Click mouse button"""
        try:
            if x and y:
                pyautogui.click(x, y, clicks=clicks, button=button)
            else:
                pyautogui.click(clicks=clicks, button=button)
            logger.info(f"Clicked {button} button {clicks} time(s)")
            return {"success": True, "message": "Click executed"}
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def type_text(text: str, interval: float = 0.05):
        """Type text"""
        try:
            pyautogui.typewrite(text, interval=interval)
            logger.info(f"Typed: {text[:50]}...")
            return {"success": True, "message": f"Typed {len(text)} characters"}
        except Exception as e:
            logger.error(f"Type failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def press_key(key: str):
        """Press a keyboard key"""
        try:
            pyautogui.press(key)
            logger.info(f"Pressed key: {key}")
            return {"success": True, "message": f"Pressed {key}"}
        except Exception as e:
            logger.error(f"Key press failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def hotkey(*keys):
        """Press key combination (e.g., Ctrl+C)"""
        try:
            pyautogui.hotkey(*keys)
            logger.info(f"Hotkey pressed: {'+'.join(keys)}")
            return {"success": True, "message": f"Hotkey {'+'.join(keys)} pressed"}
        except Exception as e:
            logger.error(f"Hotkey failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_application(app_name: str):
        """Open application"""
        try:
            system = platform.system()
            
            if system == "Windows":
                subprocess.Popen(app_name)
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif system == "Linux":
                subprocess.Popen([app_name])
            
            logger.info(f"Opened application: {app_name}")
            time.sleep(2)  # Wait for app to open
            return {"success": True, "message": f"Opened {app_name}"}
        
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_mouse_position():
        """Get current mouse position"""
        try:
            x, y = pyautogui.position()
            logger.info(f"Mouse position: ({x}, {y})")
            return {"success": True, "x": x, "y": y}
        except Exception as e:
            logger.error(f"Get position failed: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def screenshot(filename: str = "screenshot.png"):
        """Take screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            logger.info(f"Screenshot saved: {filename}")
            return {"success": True, "message": f"Screenshot saved to {filename}"}
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return {"success": False, "error": str(e)}

def execute_pc_action(params: dict):
    """Execute PC control action from API"""
    action = params.get("action_type")
    
    if action == "move_mouse":
        return PCController.move_mouse(
            params.get("x"),
            params.get("y"),
            params.get("duration", 1.0)
        )
    
    elif action == "click":
        return PCController.click(
            params.get("x"),
            params.get("y"),
            params.get("button", "left"),
            params.get("clicks", 1)
        )
    
    elif action == "type_text":
        return PCController.type_text(params.get("text", ""))
    
    elif action == "press_key":
        return PCController.press_key(params.get("key"))
    
    elif action == "hotkey":
        keys = params.get("keys", [])
        return PCController.hotkey(*keys)
    
    elif action == "open_application":
        return PCController.open_application(params.get("app_name"))
    
    elif action == "screenshot":
        return PCController.screenshot(params.get("filename", "screenshot.png"))
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}
