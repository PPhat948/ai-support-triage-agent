import os
import json
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

# Setup Path to Data Directory (relative to this script: ../data)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# logging.basicConfig(level=logging.INFO) <-- Removed global config
logger = logging.getLogger(__name__)

def ensure_data_dir():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

def create_knowledge_base_pdf(filename=DATA_DIR / "knowledge_base.pdf"):
    c = canvas.Canvas(str(filename), pagesize=letter)
    width, height = letter
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "COMPANY KNOWLEDGE BASE & POLICY MANUAL")
    y -= 30
    c.setFont("Helvetica", 10)

    # Content to Inject
    content = """
    ## SECTION 1: BILLING & SUBSCRIPTIONS

    **1. Subscription Tiers**
    * **Free Tier:** Basic access, limited to 5 projects. Community support only (response time 48-72 hours). No export features.
    * **Pro Tier:** Unlimited projects, Advanced Export (PDF/CSV), Priority Email Support (< 24 hours). Cost: $29.99/month.
    * **Enterprise Tier:** Custom seats, Dedicated Account Manager, 24/7 Phone Support, SLA Guarantee (99.9% Uptime).

    **2. Refund Policy**
    * **General Rule:** Refunds are limited to prevent abuse.
    * **Pro Plan Eligibility:** Full refund available if requested within **7 days** of the initial charge or renewal date. Requests made after 7 days are non-refundable.
    * **Enterprise Plan:** Subject to the MSA. Generally non-refundable unless there is a breach of SLA.
    * **Free Tier:** No refunds applicable.
    * **Process:** Contact billing@company.com. Allow 5-10 business days for funds to appear.

    **3. Billing Disputes & Double Charges**
    * If duplicate charges occur (e.g., clicking "Pay" twice), contact support immediately.
    * **WARNING:** Initiating a chargeback or dispute with your bank will result in **immediate account suspension**. We strongly recommend contacting Support first.

    ---

    ## SECTION 2: TECHNICAL TROUBLESHOOTING

    **4. System Requirements & Settings**
    * Supported Browsers: Chrome, Firefox, Safari (v14+).
    * **Dark Mode Support:**
        * Currently, there is **NO manual toggle** in the app.
        * **Auto-Sync:** The app automatically syncs with your OS theme. If your Mac/Windows is dark, the app will be dark.
        * *Roadmap:* Manual scheduler planned for Q3 2026.

    **5. Common Error Codes**
    * **Error 403 (Forbidden):** Free users trying to access Pro features (Export). Solution: Upgrade.
    * **Error 500 (Internal Server Error):** Server-side issue.
        * **Action:** Check status.company.com. If "Operational" but error persists for >15 mins, this is a **Critical Incident**. Enterprise users should use the emergency line.

    ---

    ## SECTION 3: SERVICE LEVEL AGREEMENT (SLA)

    **6. Priority Matrix**
    * **Low:** How-to questions, Feature requests. (Action: Auto-respond)
    * **Medium:** Bug reports (Pro), Billing disputes <$100. (Action: Route to Specialist)
    * **High:** Service unavailability (Pro), Billing disputes >$100 or legal threats. (Action: Escalate)
    * **Critical:** Total System Outage, Data Breach. (Action: Immediate Escalation to Engineering)

    **7. Regional Info**
    * **Asia-Pacific (Thailand/Vietnam):** Users may experience higher latency during peak hours (14:00 - 16:00 UTC+7) due to local ISP throttling. This is NOT a server outage unless Error 500 is observed.
    """

    lines = content.strip().split('\n')
    
    for line in lines:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        
        c.drawString(50, y, line.strip())
        y -= 15

    c.save()
    logger.info(f"✅ Generated PDF at {filename}")

def create_customer_json(filename=DATA_DIR / "customers.json"):
    data = {
        "cust_01": {
            "name": "Sarah Jenkins",
            "plan": "free",
            "region": "US",
            "history_months": 4
        },
        "cust_02": {
            "name": "TechFlow Enterprise Ltd.",
            "plan": "enterprise",
            "region": "Asia",
            "history_months": 24
        },
        "cust_03": {
            "name": "John Doe",
            "plan": "pro",
            "region": "EU",
            "history_months": 12
        }
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logger.info(f"✅ Generated Customers JSON at {filename}")

def create_system_status_json(filename=DATA_DIR / "system_status.json"):
    data = {
        "last_updated": "2025-12-14T13:45:00Z",
        "global_status": "partial_outage",
        "regions": {
            "us-east": {
                "status": "operational",
                "latency_ms": 45,
                "message": "All systems functioning normally."
            },
            "eu-west": {
                "status": "operational",
                "latency_ms": 60,
                "message": "All systems functioning normally."
            },
            "asia-pacific": {
                "status": "major_outage",
                "latency_ms": 5000,
                "message": "CRITICAL: High rate of 500 Internal Server Errors detected in Bangkok and Singapore nodes."
            }
        }
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logger.info(f"✅ Generated System Status JSON at {filename}")

def generate_all_mock_data():
    ensure_data_dir()
    create_knowledge_base_pdf()
    create_customer_json()
    create_system_status_json()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_all_mock_data()
