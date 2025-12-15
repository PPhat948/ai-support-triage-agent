# AI Support Ticket Triage Agent

This agent uses AI to analyze support tickets and route them to the correct department.

---

## Project Structure

```text
Ooca/
├── app/
│   ├── agent.py          # Configures the AI agent and defines its behavior
│   ├── main.py           # Entry point for the FastAPI application
│   ├── models.py         # Defines the data schemas for inputs and outputs
│   ├── rag_service.py    # Handles RAG logic and document retrieval
│   └── tools.py          # Contains utility functions for the agent
├── data/
│   ├── customers.json    # Mock customer dataset
│   └── knowledge_base.pdf # Mock knowledge base document
├── scripts/
│   └── setup_mock_data.py # Script to generate mock data
├── run.py               # Startup script for the Uvicorn server
└── REPORT.md            # Technical report documentation
```

### Key Components

*   **`app/agent.py`**: Orchestrates the core AI logic using LangChain. It constructs the system prompt, manages the decision-making loop, and executes the final response generation based on tool outputs.
*   **`app/tools.py`**: Provides the executable functions available to the agent, offering capability interfaces for `get_customer_profile` and `check_system_status`.
*   **`app/rag_service.py`**: Implements the Retrieval-Augmented Generation (RAG) pipeline. It manages document ingestion, embedding generation, and semantic search to retrieve relevant policy context.
*   **`app/main.py`**: Initializes the FastAPI application, configures the API router, and manages the request/response lifecycle for the inference endpoint.

## Installation

You can install dependencies using either **uv** (Recommended) or **pip**.

### Option 1: Using `uv` (Modern & Fast)
If you have `uv` installed, it directly uses `pyproject.toml`.
```bash
pip install uv
uv sync
```

### Option 2: Using `pip` (Standard)
Standard installation using the requirements file.
```bash
pip install -r requirements.txt
```

---

## Configuration

1.  **Environment Variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

---

## Running the Application

Start the FastAPI server:
```bash
python run.py
```
*The server will start at `http://127.0.0.1:8000`*

---

## Testing via Swagger UI

FastAPI provides an interactive documentation interface (Swagger UI) to test the API directly from your browser.

1.  **Open Documentation:**
    Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2.  **Select the Endpoint:**
    Click on the **POST** bar labeled `/api/triage`.

3.  **Unlock Input Mode:**
    Click the **Try it out** button (top right of the endpoint box).

4.  **Enter Request JSON:**
    In the **Request body** field, enter a test JSON.
    
    *   **Structure:**
        *   `customer_id`: ID from `data/customers.json` (e.g., `cust_01`, `cust_02`, `cust_03`).
        *   `message`: The complaint or question.

    *   **Example Input:**
        ```json
        {
          "customer_id": "cust_03",
          "message": "I am very angry! My refund hasn't arrived yet and it's been 5 days."
        }
        ```

5.  **Execute:**
    Click the big blue **Execute** button.

6.  **Check Response:**
    Scroll down to **Server response**. You will see the AI's reasoned decision:

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
