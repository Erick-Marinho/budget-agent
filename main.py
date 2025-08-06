import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",    
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Budget Agent", 
    description="Budget Agent",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/", summary="Root endpoint", description="Root endpoint for the API")
async def root():
    return {
        "message": "Budget Agent is running",
        "status": "success",
        "version": "0.1.0",
        "docs": "http://localhost:8001/docs",        
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {"status": "healthy", "service": "budget-agent"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)