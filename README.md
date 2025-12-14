# AI Support Ticket Triage Agent

This agent uses AI to analyze support tickets and route them to the correct department.

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

2.  **Generate Mock Data (Optional):**
    The app generates data automatically on first run. You can also run it manually:
    ```bash
    python -m scripts.setup_mock_data
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
    Scroll down to **Server response**. You will see the AI's reasoned decision, including:
    *   `internal_ticket_note`: Summary for your staff.
    *   `user_response`: Empathetic reply for the customer.
    *   `execution_result`: Confirmation of any simulated ticket creation.
