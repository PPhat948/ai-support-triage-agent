import json
import os
import logging
from pathlib import Path
from langchain_core.tools import tool
from app.rag_service import get_vector_store

logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Global variable to hold the vector store instance (Lazy Loading)
_vectorstore = None

def _get_retriever():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = get_vector_store()
    return _vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def get_customer_profile(customer_id: str) -> dict:
    """
    Look up a customer's profile by their ID.
    Reads from 'data/customers.json'.
    """
    logger.info(f"Tool 'get_customer_profile' called for ID: {customer_id}")
    try:
        with open(DATA_DIR / "customers.json", "r", encoding="utf-8") as f:
            customers = json.load(f)
        result = customers.get(customer_id, {"error": "Customer not found"})
        logger.info(f"Tool Result: Found profile for {result.get('name', 'Unknown')}")
        return result
    except FileNotFoundError:
        logger.error("Database error: customers.json not found")
        return {"error": "Database error: customers.json not found"}

@tool
def check_system_status(region: str) -> str:
    """
    Check the technical system status for a specific region.
    Maps input region (e.g. 'Thailand', 'Asia') to internal region keys.
    """
    logger.info(f"Tool 'check_system_status' called for region: {region}")
    try:
        with open(DATA_DIR / "system_status.json", "r", encoding="utf-8") as f:
            status_data = json.load(f)
    except FileNotFoundError:
        logger.error("system_status.json not found")
        return "Error: System status data unavailable."

    # Normalize input variations (e.g. 'thailand' -> 'asia-pacific')
    region_lower = region.lower()
    
    target_key = "unknown"
    if "asia" in region_lower or "thailand" in region_lower:
        target_key = "asia-pacific"
    elif "us" in region_lower or "america" in region_lower:
        target_key = "us-east"
    else:
        # Fallback to checking the last known statuses
        pass

    region_status = status_data["regions"].get(target_key)
    
    if region_status:
        state = region_status.get("status", "unknown")
        msg = region_status.get("message", "No details")
        
        result_str = ""
        if "outage" in state:
            result_str = f"🔴 {state.upper()}: {msg}"
        else:
            result_str = f"🟢 {state.upper()}: {msg}"
        
        logger.info(f"Tool Result: {state}")
        return result_str
            
    return "⚪ Status unknown for this region. (Check global status: " + status_data.get("global_status", "unknown") + ")"

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base (FAQs, Policies) for answers.
    Use this for feature questions, billing policies, or troubleshooting.
    """
    logger.info(f"Tool 'search_knowledge_base' searching for: '{query}'")
    retriever = _get_retriever()
    docs = retriever.invoke(query)
    logger.info(f"Tool Result: Retrieved {len(docs)} documents")
    return "\n\n".join([d.page_content for d in docs])
