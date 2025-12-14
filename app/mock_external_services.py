import uuid
import logging
import random
import time

logger = logging.getLogger(__name__)

def mock_create_ticket(department: str, priority: str, note: str) -> str:
    """
    Simulates creating a support ticket in an external CRM (e.g., Zendesk, Jira).
    """
    # Generate a random Ticket ID
    ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"
    
    # Simulate API Latency
    time.sleep(0.5) 
    
    # Log the action (This is the visible "Side Effect")
    logger.info(f"--------- [MOCK CRM API CALL] ---------")
    logger.info(f"Creating Ticket ID: {ticket_id}")
    logger.info(f"Target Dept: {department} | Priority: {priority}")
    logger.info(f"Internal Note: {note}")
    logger.info(f"---------------------------------------")
    
    return ticket_id
