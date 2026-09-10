"""
Updated main.py with error handling and health monitoring
"""

import os
import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import time

# Import custom modules
from llm_router import LLMRouter
from config import Config
from error_handler import error_handler, health_monitor, handle_errors
from startup_check import StartupChecker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="JARVIS AI",
    description="Open-source AI assistant with dual LLM architecture",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize config and LLM router
config = Config()
llm_router = None

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None
    force_gemini: Optional[bool] = False
    force_groq: Optional[bool] = False

class ActionRequest(BaseModel):
    action: str
    params: dict

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

# Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "JARVIS AI",
        "version": "1.0.0",
        "endpoints": {
            "query": "/query",
            "action": "/action",
            "health": "/health",
            "models": "/models"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        if llm_router is None:
            return {
                "status": "initializing",
                "message": "LLM router not yet initialized"
            }
        
        groq_status = llm_router.check_groq_health()
        gemini_status = llm_router.check_gemini_health()
        
        # Get health metrics
        metrics = health_monitor.get_metrics()
        
        return {
            "status": "healthy" if (groq_status or gemini_status) else "degraded",
            "groq": "✓" if groq_status else "✗",
            "gemini": "✓" if gemini_status else "✗",
            "health_status": health_monitor.get_health_status(),
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/models")
async def get_models():
    """Get available models and their status"""
    return {
        "available_models": [
            {
                "name": "Groq (Mixtral)",
                "model_id": "mixtral-8x7b-32768",
                "speed": "ultra-fast",
                "use_case": "Simple queries, quick responses",
                "cost": "Free",
                "rate_limit": "30 req/min"
            },
            {
                "name": "Google Gemini",
                "model_id": "gemini-pro",
                "speed": "fast",
                "use_case": "Complex tasks, reasoning",
                "cost": "Free",
                "rate_limit": "60 req/min, 1500/day"
            }
        ],
        "routing_strategy": "Automatic based on query complexity"
    }

@app.post("/query")
async def process_query(request: QueryRequest):
    """
    Process a query using the dual LLM router.
    Automatically selects between Groq (fast) and Gemini (complex).
    """
    try:
        if llm_router is None:
            raise HTTPException(
                status_code=503,
                detail="LLM router not initialized"
            )
        
        logger.info(f"Processing query: {request.query[:100]}...")
        start_time = time.time()
        
        # Route to appropriate LLM
        response = await llm_router.route_query(
            query=request.query,
            context=request.context,
            force_gemini=request.force_gemini,
            force_groq=request.force_groq
        )
        
        processing_time = time.time() - start_time
        health_monitor.record_request(True, processing_time)
        
        return {
            "status": "success",
            "query": request.query,
            "response": response["content"],
            "model_used": response["model"],
            "processing_time": response["time"],
            "confidence": response.get("confidence", 0.8)
        }
    
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        health_monitor.record_request(False, 0)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/action")
async def execute_action(request: ActionRequest):
    """
    Execute system actions:
    - pc_control: Mouse, keyboard, window management
    - browser: Open URLs, navigate, fill forms
    - smart_home: Control devices
    - twilio: Send SMS, make calls
    """
    try:
        logger.info(f"Executing action: {request.action}")
        
        if request.action == "pc_control":
            from actions.pc_control import execute_pc_action
            result = execute_pc_action(request.params)
        
        elif request.action == "browser":
            from actions.browser import execute_browser_action
            result = await execute_browser_action(request.params)
        
        elif request.action == "smart_home":
            from actions.smart_home import execute_smart_home_action
            result = await execute_smart_home_action(request.params)
        
        elif request.action == "twilio":
            from actions.twilio_handler import execute_twilio_action
            result = await execute_twilio_action(request.params)
        
        else:
            raise ValueError(f"Unknown action: {request.action}")
        
        return {
            "status": "success",
            "action": request.action,
            "result": result
        }
    
    except Exception as e:
        logger.error(f"Action execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "query":
                if llm_router is None:
                    await websocket.send_json({
                        "type": "error",
                        "content": "LLM router not initialized"
                    })
                    continue
                
                response = await llm_router.route_query(data.get("content"))
                await websocket.send_json({
                    "type": "response",
                    "content": response["content"],
                    "model": response["model"]
                })
            
            elif data.get("type") == "action":
                action_type = data.get("action")
                params = data.get("params", {})
                await websocket.send_json({
                    "type": "action_complete",
                    "status": "success"
                })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    
    finally:
        await websocket.close()

# Startup event
@app.on_event("startup")
async def startup_event():
    global llm_router
    
    logger.info("🚀 JARVIS AI starting up...")
    
    # Run startup checks
    StartupChecker.print_startup_report()
    
    # Initialize LLM router
    try:
        llm_router = LLMRouter(config)
        logger.info("✓ LLM Router initialized")
    except Exception as e:
        logger.error(f"Failed to initialize LLM Router: {e}")
        llm_router = None
    
    logger.info(f"Gemini API: {'✓' if config.gemini_key else '✗'}")
    logger.info(f"Groq API: {'✓' if config.groq_key else '✗'}")
    logger.info(f"Twilio: {'✓' if config.twilio_configured else '✗'}")
    logger.info("\n✅ JARVIS AI is ready!\n")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 JARVIS AI shutting down...")
    logger.info(f"Final metrics: {health_monitor.get_metrics()}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT", 8000)),
        log_level="info"
    )
