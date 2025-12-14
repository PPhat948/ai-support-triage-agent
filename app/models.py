from pydantic import BaseModel, Field
from typing import Literal, Optional

class TicketResolution(BaseModel):
    urgency: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="The urgency level of the ticket."
    )
    issue_type: Literal["Billing", "Technical", "Feature Request", "General Inquiry"] = Field(
        ..., description="The category of the issue."
    )
    sentiment: Literal["positive", "neutral", "negative", "frustrated"] = Field(
        ..., description="The implied sentiment of the customer."
    )
    action: Literal["auto_respond", "route_to_specialist", "escalate_to_human"] = Field(
        ..., description="The recommended next action."
    )
    target_department: Optional[Literal["Billing", "Sales", "Support", "Engineering", "Product"]] = Field(
        None, description="The department to route the ticket to (if applicable)."
    )
    internal_ticket_note: str = Field(
        ..., description="FOR STAFF: Concise, fact-based summary of the issue."
    )
    user_response: str = Field(
        ..., description="FOR USER: A polite, empathetic response addressing the user directly."
    )
    executed_tools: list[str] = Field(
        ..., description="A list of the exact tool names called during the process."
    )
    reasoning_trace: str = Field(
        ..., description="A concise summary of the logic used to make the decision."
    )
