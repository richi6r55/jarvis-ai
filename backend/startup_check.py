"""
Configuration validation and health checks
"""

import os
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

class ConfigValidator:
    """Validate configuration and dependencies"""
    
    @staticmethod
    def validate_api_keys() -> Tuple[bool, List[str]]:
        """Check if required API keys are set"""
        issues = []
        
        gemini_key = os.getenv("GEMINI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        
        if not gemini_key:
            issues.append("⚠️  GEMINI_API_KEY not set - complex queries will fail")
        
        if not groq_key:
            issues.append("⚠️  GROQ_API_KEY not set - fast queries will fail")
        
        if gemini_key and groq_key:
            return True, []
        
        return False, issues
    
    @staticmethod
    def validate_optional_services() -> dict:
        """Check optional service configurations"""
        services = {
            'twilio': {
                'configured': all([
                    os.getenv("TWILIO_ACCOUNT_SID"),
                    os.getenv("TWILIO_AUTH_TOKEN"),
                    os.getenv("TWILIO_PHONE")
                ]),
                'missing': []
            },
            'smart_home': {
                'configured': bool(os.getenv("HOME_ASSISTANT_TOKEN")),
                'url': os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")
            }
        }
        
        # Check Twilio
        if not services['twilio']['configured']:
            required = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE']
            services['twilio']['missing'] = [
                key for key in required if not os.getenv(key)
            ]
        
        return services
    
    @staticmethod
    def validate_dependencies() -> Tuple[bool, List[str]]:
        """Check if required Python packages are installed"""
        issues = []
        required_packages = [
            ('fastapi', 'FastAPI'),
            ('uvicorn', 'Uvicorn'),
            ('pydantic', 'Pydantic'),
            ('aiohttp', 'aiohttp'),
        ]
        
        for package, name in required_packages:
            try:
                __import__(package)
            except ImportError:
                issues.append(f"Missing: {name} (pip install {package})")
        
        # Check optional packages
        optional_packages = [
            ('groq', 'Groq API'),
            ('google.generativeai', 'Google Generative AI'),
            ('playwright', 'Playwright (Browser automation)'),
            ('pyautogui', 'PyAutoGUI (PC control)'),
            ('twilio', 'Twilio (SMS/Voice)'),
        ]
        
        optional_issues = []
        for package, name in optional_packages:
            try:
                __import__(package.split('.')[0])
            except ImportError:
                optional_issues.append(f"Optional: {name} (pip install {package.split('.')[0]})")
        
        return len(issues) == 0, issues + optional_issues
    
    @classmethod
    def validate_all(cls) -> dict:
        """Run all validations"""
        api_ok, api_issues = cls.validate_api_keys()
        dep_ok, dep_issues = cls.validate_dependencies()
        optional_services = cls.validate_optional_services()
        
        return {
            'api_keys': {
                'valid': api_ok,
                'issues': api_issues
            },
            'dependencies': {
                'valid': dep_ok,
                'issues': dep_issues
            },
            'optional_services': optional_services,
            'overall': api_ok and dep_ok
        }

class StartupChecker:
    """Check system before startup"""
    
    @staticmethod
    def print_startup_report():
        """Print detailed startup report"""
        print("\n" + "="*60)
        print("🚀 JARVIS AI - Startup Check")
        print("="*60 + "\n")
        
        validation = ConfigValidator.validate_all()
        
        # API Keys Status
        print("🔑 API Keys:")
        if validation['api_keys']['valid']:
            print("  ✓ All required API keys configured")
        else:
            for issue in validation['api_keys']['issues']:
                print(f"  {issue}")
        print()
        
        # Dependencies Status
        print("📦 Dependencies:")
        if validation['dependencies']['valid']:
            print("  ✓ All required packages installed")
        else:
            for issue in validation['dependencies']['issues']:
                print(f"  ⚠️  {issue}")
        print()
        
        # Optional Services
        print("🔧 Optional Services:")
        if validation['optional_services']['twilio']['configured']:
            print("  ✓ Twilio configured")
        else:
            print("  ⚠️  Twilio not configured")
        
        if validation['optional_services']['smart_home']['configured']:
            print(f"  ✓ Smart Home (Home Assistant) configured")
        else:
            print("  ⚠️  Smart Home not configured")
        print()
        
        # Overall Status
        print("="*60)
        if validation['overall']:
            print("✅ Ready to start! All required components are available.")
        else:
            print("⚠️  Some issues detected. See above for details.")
            print("\n📖 Get started:")
            print("  1. Get GEMINI_API_KEY: https://aistudio.google.com/")
            print("  2. Get GROQ_API_KEY: https://groq.com/ai/")
            print("  3. Edit .env file with your keys")
            print("  4. Restart the application")
        print("="*60 + "\n")
        
        return validation
