"""
Browser Automation Module - Navigate, interact with websites
"""

import logging
import asyncio
from typing import Dict, Optional

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger(__name__)

class BrowserController:
    """Handle browser automation"""
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    async def init_browser(self):
        """Initialize browser"""
        try:
            if not PLAYWRIGHT_AVAILABLE:
                raise Exception("Playwright not installed")
            
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            logger.info("✓ Browser initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return False
    
    async def navigate(self, url: str):
        """Navigate to URL"""
        try:
            if not self.page:
                await self.init_browser()
            
            await self.page.goto(url, wait_until="domcontentloaded")
            logger.info(f"Navigated to: {url}")
            return {"success": True, "url": url}
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def fill_input(self, selector: str, text: str):
        """Fill input field"""
        try:
            if not self.page:
                return {"success": False, "error": "Browser not initialized"}
            
            await self.page.fill(selector, text)
            logger.info(f"Filled input: {selector}")
            return {"success": True, "message": f"Filled {selector}"}
        except Exception as e:
            logger.error(f"Fill failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def click_button(self, selector: str):
        """Click button"""
        try:
            if not self.page:
                return {"success": False, "error": "Browser not initialized"}
            
            await self.page.click(selector)
            logger.info(f"Clicked: {selector}")
            return {"success": True, "message": f"Clicked {selector}"}
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_text(self, selector: str):
        """Extract text from element"""
        try:
            if not self.page:
                return {"success": False, "error": "Browser not initialized"}
            
            text = await self.page.text_content(selector)
            logger.info(f"Extracted text from: {selector}")
            return {"success": True, "text": text}
        except Exception as e:
            logger.error(f"Get text failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def screenshot(self, filename: str = "browser_screenshot.png"):
        """Take browser screenshot"""
        try:
            if not self.page:
                return {"success": False, "error": "Browser not initialized"}
            
            await self.page.screenshot(path=filename)
            logger.info(f"Screenshot saved: {filename}")
            return {"success": True, "filename": filename}
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def close(self):
        """Close browser"""
        try:
            if self.browser:
                await self.browser.close()
            logger.info("Browser closed")
            return True
        except Exception as e:
            logger.error(f"Failed to close browser: {e}")
            return False

# Global browser instance
_browser_instance = None

async def get_browser() -> BrowserController:
    """Get or create browser instance"""
    global _browser_instance
    if _browser_instance is None:
        _browser_instance = BrowserController()
        await _browser_instance.init_browser()
    return _browser_instance

async def execute_browser_action(params: dict) -> Dict:
    """Execute browser action from API"""
    action = params.get("action_type")
    browser = await get_browser()
    
    if action == "navigate":
        return await browser.navigate(params.get("url"))
    
    elif action == "fill_input":
        return await browser.fill_input(
            params.get("selector"),
            params.get("text")
        )
    
    elif action == "click":
        return await browser.click_button(params.get("selector"))
    
    elif action == "get_text":
        return await browser.get_text(params.get("selector"))
    
    elif action == "screenshot":
        return await browser.screenshot(params.get("filename", "browser_screenshot.png"))
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}
