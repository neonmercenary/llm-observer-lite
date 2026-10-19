# llm-observability-lite 📊🔍

**llm-observability-lite** is a lightweight, local-first backend engineering and observability tool designed to track, log, and visualize LLM request telemetry. Built with zero bloat, it captures request IDs, execution latency, token counts, success/error statuses, and model identity, rendering it all in a real-time dashboard.

---

## 🚀 Key Features

* **Real-Time Telemetry Tracking:** Automatically logs every model run, capturing request timestamps, unique IDs, and performance metrics.
* **Success & Failure Tracing:** Captures both successful model executions and deliberate/accidental runtime failures with detailed error logs.
* **Performance Visualization:** Includes an embedded **Chart.js** dashboard tracking the latency performance of your recent model tasks.
* **Lightweight & Self-Contained:** Powered entirely by **FastAPI**, **SQLite**, and vanilla HTML/CSS with no heavy cloud infrastructure or external SaaS dependencies.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python 3.11+)
* **Database:** SQLite (`observability.db`)
* **Frontend Dashboard:** HTML5, CSS3, Chart.js (via CDN)
* **Package Management:** `uv`

---

## 📂 Project Structure

```text
llm-observability-lite/
├── app/
│   ├── __init__.py
│   ├── database.py    # SQLite log storage setup and schema initialization
│   └── main.py        # FastAPI app with telemetry simulation and logging
├── static/
│   └── index.html     # Dashboard frontend with Chart.js visualizer & control panel
├── pyproject.toml
└── README.md

```

---

## ⚙️ Getting Started

### 1. Prerequisites

Ensure you have Python 3.11+ and `uv` installed.

### 2. Installation

Clone the repository and install dependencies using `uv`:

```bash
git clone [https://github.com/yourusername/llm-observability-lite.git](https://github.com/yourusername/llm-observability-lite.git)
cd llm-observability-lite
uv sync

```

### 3. Run the Application

Start the FastAPI server via command line:

```bash
python -m uvicorn app.main:app --reload

```

Open your browser and navigate to **`http://127.0.0.1:8000`** to access the observability dashboard.

---

## 🔌 API Endpoints

* **`POST /api/v1/infer`**
* Simulates or triggers a model inference task.
* Accepts a JSON payload (`prompt`, `model_name`, `simulate_error`) and logs the execution duration and status to SQLite.


* **`GET /api/v1/logs`**
* Fetches the recent request trace logs from the database for dashboard rendering.



---

## 🎯 Verification (Definition of Done)

1. Open the dashboard at `http://127.0.0.1:8000`.
2. Click **"Run Success Task"** to generate successful requests.
3. Click **"Trigger Deliberate Failure"** to log error states.
4. Verify that both appear instantly in the telemetry history table and update the Chart.js latency visualizer.

```
