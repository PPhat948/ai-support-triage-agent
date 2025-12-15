# AI Support Ticket Triage Agent

This project implements an AI-powered support ticket triage agent that analyzes incoming support tickets and automatically routes them to the appropriate department based on customer context, sentiment, and business rules.

---

## Project Structure

```text
Ooca/
├── app/
│   ├── agent.py           # Configures the AI agent and defines its behavior
│   ├── main.py            # Entry point for the FastAPI application
│   ├── models.py          # Defines the data schemas for inputs and outputs
│   ├── rag_service.py     # Handles RAG logic and document retrieval
│   └── tools.py           # Contains utility functions for the agent
├── data/
│   ├── customers.json     # Mock customer dataset
│   └── knowledge_base.pdf # Mock knowledge base document
├── scripts/
│   └── setup_mock_data.py # Script to generate mock data
├── run.py                 # Startup script for the Uvicorn server
└── REPORT.md              # Technical report documentation
```

---

## Key Components

* **app/agent.py**: Orchestrates the core AI logic using LangChain, including prompt construction, reasoning flow, and final decision generation.
* **app/tools.py**: Defines callable tools such as `get_customer_profile` and `check_system_status` that the agent can use during reasoning.
* **app/rag_service.py**: Implements the Retrieval-Augmented Generation (RAG) pipeline for policy and knowledge lookup.
* **app/main.py**: Initializes the FastAPI application and manages the request/response lifecycle.

---

## Installation

You can install dependencies using either **uv** (recommended) or **pip**.

### Option 1: Using `uv` (Recommended)

`uv` installs dependencies directly from `pyproject.toml` and manages its own virtual environment.

```bash
pip install uv
uv sync
```

### Option 2: Using `pip`

Standard installation using a requirements file.

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root and set your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Application

### Option 1: Running with `uv`

If dependencies were installed using `uv sync`, you must run the application through `uv` to ensure the correct environment is used.

```bash
uv run python run.py
```

The FastAPI server will start at:

```
http://127.0.0.1:8000
```

---

### Option 2: Running with `pip`

If dependencies were installed using `pip install -r requirements.txt`, run the application directly with Python.

```bash
python run.py
```

The FastAPI server will start at:

```
http://127.0.0.1:8000
```

---

**Note:** Do not mix installation and runtime methods.

* Use `uv run` if you installed dependencies with `uv sync`.
* Use `python run.py` if you installed dependencies with `pip`.

---

## Testing via Swagger UI

FastAPI provides an interactive Swagger UI for testing the API.

1. Open the documentation:

   ```
   http://127.0.0.1:8000/docs
   ```

2. Select the **POST** endpoint `/api/triage`.

3. Click **Try it out**.

4. Provide a request body with the following fields:

   * `customer_id`: An ID from `data/customers.json` (e.g., `cust_01`, `cust_02`, `cust_03`).
   * `message`: The customer complaint or question.

### Example Request

```json
{
  "customer_id": "cust_03",
  "message": "I am very angry! My refund hasn't arrived yet and it's been 5 days."
}
```

### Example Response

```json
{
  "decision": {
    "urgency": "medium",
    "issue_type": "Technical",
    "sentiment": "frustrated",
    "action": "route_to_specialist",
    "target_department": "Support",
    "internal_ticket_note": "User (Pro) cannot login. System normal. Routing to support.",
    "user_response": "I understand you can't login. Our systems are running normally, so I've escalated this to a support specialist to investigate further.",
    "executed_tools": [
      "get_customer_profile",
      "check_system_status"
    ],
    "reasoning_trace": "Customer Plan is Pro. System Status is Operational. The issue is a technical access problem, not an outage. Therefore, the urgency is MEDIUM and the action is to route to a specialist."
  },
  "execution_result": {
    "status": "ticket_routed",
    "ticket_id": "TKT-B489E2",
    "message": "Case routed to Support specialist."
  }
}
```
