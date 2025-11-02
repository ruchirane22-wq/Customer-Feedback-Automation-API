# Customer Feedback Automation API

**Language:** Python (Flask)  
**Domain used for generated links:** `tatamotors.com`  
**Database:** SQLite (lightweight, file-based - `feedback.db`)

## Overview
This project provides a simple REST API to automatically generate customer feedback links based on service request details.
It stores generated links in a local SQLite database for traceability and analytics.

## Endpoints
- `POST /create-feedback-link`  
  **Request JSON**
  ```json
  {
    "cust_sr_no": "SR-Jagdale/VP-2425-002646",
    "cust_mob_no": "9960348514",
    "cust_veh_no": "MH41Y1393"
  }
  ```
  **Response**
  ```json
  {
    "cust_sr_no": "...",
    "cust_mob_no": "...",
    "cust_veh_no": "...",
    "link": "https://feedback.tatamotors.com/feedback/<id>",
    "feedback_id": "<id>",
    "created_at": "<timestamp>"
  }
  ```

- `GET /links`  
  Returns the latest saved feedback link records (up to 100).

- `GET /health`  
  Simple health check endpoint.

## How to run (local)
1. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the app
```bash
python app.py
```
4. Test with `curl` or Postman:
```bash
curl -X POST http://127.0.0.1:5000/create-feedback-link \
  -H "Content-Type: application/json" \
  -d '{"cust_sr_no":"SR-123","cust_mob_no":"9999999999","cust_veh_no":"MH01AB1234"}'
```

## Folder structure
```
Customer-Feedback-Automation-API/
├── app.py
├── requirements.txt
├── README.md
├── sample_request.json
└── feedback.db    # created automatically on first run
```

## Next steps / Enhancements
- Add authentication (API key / OAuth) for secure link creation.
- Integrate with a proper RDBMS (SQL Server / PostgreSQL) for production.
- Add rate-limiting and input sanitization.
- Add an admin dashboard to view/link search and export logs.
- Add tests (pytest) and CI workflow.

## Author
Generated for: **Ruchi Rane** (Customer Feedback Automation API sample project)
