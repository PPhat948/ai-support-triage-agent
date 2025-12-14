from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from app.agent import run_agent
from app.models import TicketResolution
from app.mock_external_services import mock_create_ticket
from typing import Optional
import os
import logging
from pathlib import Path

# Path Config
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

# Configure basic logging to capture agent activity.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "agent_activity.log")
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Support Ticket Triage Agent")

# --- Models ---
class TriageRequest(BaseModel):
    message: str
    customer_id: str

class ExecutionResult(BaseModel):
    status: str
    ticket_id: Optional[str] = None
    message: str

class TriageResponse(BaseModel):
    decision: TicketResolution
    execution_result: ExecutionResult

# --- Startup ---
@app.on_event("startup")
async def startup_event():
    # Verify API Key
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not found in environment!")
    # Pre-load vector store
    from app.rag_service import get_vector_store
    try:
        get_vector_store()
        logger.info("Application startup complete. Vector store loaded.")
    except Exception as e:
        logger.warning(f"Vector store load failed: {e}")

# --- Endpoints ---
@app.get("/")
async def root():
    return {"message": "Support Triage Agent API is running. Go to /docs for Swagger UI."}

@app.post("/api/triage", response_model=TriageResponse)
async def triage_ticket(request: TriageRequest):
    logger.info(f"Received Triage Request | Customer: {request.customer_id}")
    try:
        # 1. Run Agent
        decision = run_agent(request.message, request.customer_id)
        logger.info(f"Agent Decision | Action: {decision.action} | Urgency: {decision.urgency}")
        logger.info(f"Reasoning: {decision.reasoning_trace}")
        logger.info(f"Tools Used: {decision.executed_tools}")
        
        # 2. Execution Layer: Decide whether to act or just reply.
        exec_result = ExecutionResult(status="no_action_needed", message="Auto-response handled by Agent.")
        
        if decision.action == "escalate_to_human":
            # Real-world Side Effect: Create a ticket in the external CRM.
            ticket_id = mock_create_ticket(
                department=decision.target_department or "Support",
                priority=decision.urgency,
                note=decision.internal_ticket_note
            )
            exec_result = ExecutionResult(
                status="ticket_created",
                ticket_id=ticket_id,
                message=f"Case escalated to {decision.target_department}."
            )
            
        elif decision.action == "route_to_specialist":
             # Route to specialized queue (e.g. Tier 2 Support) without immediate escalation.
            ticket_id = mock_create_ticket(
                department=decision.target_department or "Support",
                priority=decision.urgency,
                note=decision.internal_ticket_note
            )
            exec_result = ExecutionResult(
                status="ticket_routed",
                ticket_id=ticket_id,
                message=f"Case routed to {decision.target_department} specialist."
            )

        # 3. Return the comprehensive result: Decision Analysis + System Actions Taken.
        return TriageResponse(
            decision=decision,
            execution_result=exec_result
        )
        
    except Exception as e:
        logger.error(f"Error processing ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
