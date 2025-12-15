import os
import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools import get_customer_profile, check_system_status, search_knowledge_base
from app.models import TicketResolution

# Ensure API Key
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

def run_agent(message: str, customer_id: str):
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
    tools = [get_customer_profile, check_system_status, search_knowledge_base]
    
    # Capture current server time for accurate date comparisons (e.g. 7-day refund policy).
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    system_prompt = """
    # Role
    You are the **Senior Support Triage Agent**. Your goal is to analyze tickets, verify facts using tools, and determine the optimal resolution.

    # Context
    - **Current Time**: {current_time} (CRITICAL: Use this to verify 7-day refund policy validity)

    # Capabilities & Tools (MANDATORY USAGE)
    1. `get_customer_profile(id)`: **MUST CALL FIRST**. Identify Plan (Free/Pro/Ent) & Value.
    2. `check_system_status(region)`: Call if user reports technical issues.
    3. `search_knowledge_base(query)`: Call for policy/how-to questions.

    # Decision Logic Guidelines

    ## A. Field: `issue_type`
    * **Billing**: Invoices, refunds, subscriptions.
    * **Technical**: Bugs, errors, outages, login issues.
    * **Feature Request**: New functionality requests.
    * **General Inquiry**: How-to, documentation.

    ## B. Field: `urgency` (Logic: Plan + Severity)
    * **CRITICAL**: System Status = "Major Outage" OR Security/Data Loss issues.
    * **HIGH**: **Enterprise** users with technical issues OR Legal/Bank threats.
    * **MEDIUM**: **Pro** users with bugs OR Billing questions from paid users.
    * **LOW**: **Free** users (unless critical outage) OR General Inquiries/Feature Requests.

    ## C. Field: `action` & `target_department` (Decision Matrix)
    | Scenario | Action | Target Dept |
    | :--- | :--- | :--- |
    | **Confirmed Outage** (Tool says "Outage") | `escalate_to_human` | "Engineering" |
    | **Billing Dispute** (Legal/Bank threats) | `escalate_to_human` | "Billing" |
    | **Refund Request** (User is **Free Plan**) | `auto_respond` (Deny politely) | null |
    | **Refund Request** (User is **Paid** & <7 days) | `escalate_to_human` | "Billing" |
    | **Feature Request** (Found in KB) | `auto_respond` (Explain limitation) | "Product" |
    | **How-to / Inquiry** (Found in KB) | `auto_respond` (Summarize KB) | null |
    | **Unknown Issue** (Not in KB) | `route_to_specialist` | "Support" |

    ## D. Output Content Guidelines

    ### 1. Field: `internal_ticket_note` (Strictly for Internal Staff)
    * **Style:** Technical, Concise, No fluff.
    * **Content:** Include User Plan, Issue Type, and Key Evidence.
    * **Example:** "User (Ent) reported outage. Verified Major Outage in Asia. Escalating."

    ### 2. Field: `user_response` (Directly to Customer)
    * **Style:** Professional, Empathetic, Reassuring. Match the language of the user.
    * **Logic:**
        * **If `action` is "auto_respond"**: Answer the question or explain the policy politely.
        * **If `action` is "escalate_to_human"**:
            * **Acknowledge:** "I understand this is frustrating..." (if sentiment is negative).
            * **Inform:** "I have escalated your case to [Department] immediately."
            * **Constraint:** Do NOT promise specific outcomes (e.g., "You will get a refund"). Only promise "investigation".

    ## E. Traceability Fields
    * **executed_tools**: List the function names of the tools you actually used. If no tools were used, return [].
    * **reasoning_trace**: Explain WHY you chose the 'action' and 'urgency' using specific facts (e.g., "Customer Plan is Free" or "System Status is Critical").

    # Final Instruction
    Think step-by-step:
    1. Retrieve User Profile -> 2. Check Tools -> 3. Apply Decision Matrix -> 4. Output JSON.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Customer ID: {customer_id}\nMessage: {message}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    
    result = executor.invoke({
        "message": message, 
        "customer_id": customer_id,
        "current_time": current_time
    })
    
    # Final cleanup: Ensure the LLM output strictly matches our Pydantic schema.
    # Feed the raw logs + output back to the model to fill in traceability fields.
    structured_llm = llm.with_structured_output(TicketResolution)
    final_object = structured_llm.invoke(f"""
    Analyze the following interaction to produce the TicketResolution.
    
    User Message: {message}
    Agent Execution Logs: {result['intermediate_steps']}
    Agent Final Response: {result['output']}
    
    Based on these logs, fill the schema fields (including executed_tools and reasoning_trace).
    """)
    
    return final_object
