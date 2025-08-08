import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from app.application.agent.budget_agent_builder import BudgetAgentBuilder
from langchain_core.messages import HumanMessage
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

# Inicializa o budget agent
budget_agent = BudgetAgentBuilder().compile()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/", summary="Root endpoint", description="Root endpoint for the API")
async def root():
    return {
        "message": "Budget Agent is running",
        "status": "success",
        "version": "0.1.0",
        "docs": "http://localhost:8001/docs",        
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        initial_state = {"messages": [HumanMessage(content=request.message)]}
        
        result = await budget_agent.ainvoke(initial_state)
        
        last_message = result["messages"][-1]
        response_text = last_message.content
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        return ChatResponse(response="Desculpe, ocorreu um erro interno.")

@app.post("/test")
async def test_agent():
    test_request = ChatRequest(message="Quanto custa limpeza de sofá 2 lugares?")
    
    try:
        response = await chat(test_request)
        return {
            "test_status": "success",
            "agent_response": response.response
        }
    except Exception as e:
        return {
            "test_status": "error",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "budget-agent"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)