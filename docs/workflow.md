# ⚙️ ScalpStorm Workflow Document

**Version: 1.0.0**

---

## 🎯 **OVERVIEW: PROFESSIONAL CRYPTOCURRENCY TRADING**

ScalpStorm is a sophisticated, enterprise-grade cryptocurrency trading bot designed for professional traders. It offers advanced automation, risk management, and multi-bot trading capabilities across multiple exchanges, all integrated within a modern microservices architecture.

---

## 🚀 **CORE WORKFLOW: FROM SETUP TO AUTOMATED TRADING**

The ScalpStorm platform orchestrates a complex workflow to manage automated cryptocurrency trading operations.

### **1. System Initialization & Configuration**

**Function:** The application starts by initializing its FastAPI backend, connecting to MongoDB and Redis, and loading trading configurations. The frontend (React) then loads, performs health checks, and presents the user interface.

**Associated Files:**
*   **`V1_EOL/backend/server.py`**: The main FastAPI backend application. It handles startup events, database connections, and API route definitions. This is where core services are initialized.
*   **`config.py`**: Defines application-wide settings, including MongoDB connection details, API environment (demo/live), and logging levels.
*   **`secure_logging.py` (imported by `server.py`)**: Configures secure logging to prevent sensitive data exposure.
*   **`V1_EOL/frontend/frontend_simple.html`**: The main HTML file for the frontend, which loads the necessary JavaScript to run the React application.

---

### **2. User Configuration & Bot Creation**

**Function:** Users configure their exchange API credentials (Blofin, Binance.US, Binance.com) and create multiple trading bots, each with its own parameters like trading pairs, risk level, and position size.

**Associated Files:**
*   **`V1_EOL/backend/server.py`**: Contains API endpoints for `POST /api/configure` (to save exchange credentials) and `POST /api/positions` (to create new trading bots/positions). It also handles data validation using Pydantic models.
*   **`V1_EOL/backend/models.py`**: Defines Pydantic models like `TradingConfig` (for exchange credentials and global settings) and `OrderRequest` (for individual trade orders).
*   **Frontend Components (Conceptual - not explicitly listed in file overview, but implied by `frontend_simple.html`):** User interface elements in the frontend would provide forms for inputting API keys, selecting exchanges, and configuring bot parameters.

---

### **3. Market Data Acquisition & Analysis**

**Function:** The system fetches real-time market data from configured exchanges and performs advanced technical analysis to generate trading signals and recommendations.

**Associated Files:**
*   **`engine/__init__.py` (Conceptual)**: This directory likely contains the core trading logic, including market data acquisition and technical analysis algorithms. (Exact files not in the provided list, but implied by structure).
*   **`exchange_apis/__init__.py` (Conceptual)**: This directory would contain modules for integrating with different exchange APIs (e.g., Blofin, Binance.US, Binance.com) to fetch market data and execute trades.
*   **`V1_EOL/backend/server.py`**: Exposes API endpoints like `GET /api/market/pairs` (to get available trading pairs), `GET /api/market/data/{inst_id}` (for instrument-specific market data), and `GET /api/analyze/{inst_id}` (to get trading signals).
*   **`ai_integration/shenron_reporter.py`**: This module integrates with an external AI service (SHENRON) to potentially get AI trading recommendations or report anomalies based on market data.

---

### **4. Risk Management**

**Function:** Ensures trades adhere to predefined risk parameters, including position sizing, stop-loss limits, and profit targets, to protect capital.

**Associated Files:**
*   **`risk_management/risk_manager.py`**: This file (or a related one in the `risk_management` directory) would implement the core risk management logic, calculating position sizes, enforcing stop-loss/profit-target rules, and managing overall risk exposure.
*   **`risk_management/circuit_breaker.py`**: Implements a circuit breaker pattern to prevent catastrophic losses during volatile market conditions or system failures.
*   **`V1_EOL/backend/server.py`**: Integrates risk management logic into trade execution, ensuring that all orders comply with risk policies before being sent to the exchange.
*   **`V1_EOL/backend/models.py`**: `TradingConfig` model includes fields for `risk_level`, `custom_risk_percentage`, and `max_position_size` to configure risk parameters.

---

### **5. Automated Trade Execution**

**Function:** Based on market analysis and risk management, the system automatically places buy or sell orders on the configured exchanges.

**Associated Files:**
*   **`V1_EOL/backend/server.py`**: Contains API endpoints for `POST /api/positions/{position_id}/start` (to initiate trading for a bot) and `POST /api/positions/{position_id}/stop` (to stop trading). The trade execution logic would be within the FastAPI routes, interacting with `exchange_apis`.
*   **`exchange_apis/__init__.py` (Conceptual)**: Contains the client implementations for sending actual trade orders to various exchanges.
*   **`V1_EOL/backend/models.py`**: `OrderRequest` model defines the structure for placing market or limit orders.

---

### **6. Monitoring & Reporting**

**Function:** Provides real-time statistics on bot performance, system health, and logs all trading activity and anomalies.

**Associated Files:**
*   **`monitoring/__init__.py` (Conceptual)**: This directory likely contains modules for collecting performance metrics, system health, and other monitoring data.
*   **`ai_integration/shenron_reporter.py`**: Reports trade execution data, daily statistics, and anomalies to an external SHENRON dashboard for advanced AI-powered analytics.
*   **`V1_EOL/backend/server.py`**: Exposes API endpoints like `GET /api/health` (for system health checks) and `GET /api/bots/statistics` (for bot performance metrics). It also uses `secure_logging.py` for comprehensive logging.
*   **`secure_logging.py`**: Provides secure and structured logging for all critical application events, including trade executions, errors, and configuration changes.
*   **`V1_EOL/backend/frontend/frontend_simple.html`**: The frontend UI would display these real-time statistics and alerts to the user.

---

### **7. Deployment & Management**

**Function:** Provides tools and configurations for containerized deployment (Docker), allowing easy setup, scaling, and management of the ScalpStorm application.

**Associated Files:**
*   **`deployment/Dockerfile`**: Defines the Docker image for the core ScalpStorm application (though the main `Dockerfile` is under `V1_EOL/backend/Dockerfile` in the current structure, indicating an older version or a specific backend service).
*   **`V1_EOL/backend/Dockerfile`**: Defines the Docker image for the FastAPI backend service.
*   **`V1_EOL/frontend/Dockerfile.simple`**: Defines the Docker image for the simple frontend.
*   **`V1_EOL/docker-compose.yml`**: Orchestrates the multi-service Docker deployment, defining how the backend, frontend, MongoDB, and Redis containers interact.
*   **`V1_EOL/start_scalpstorm.bat` / `V1_EOL/start_scalpstorm.sh`**: Helper scripts for quickly starting the entire ScalpStorm stack using `docker-compose` on Windows and Linux/macOS respectively.
*   **`requirements.txt` / `V1_EOL/backend/requirements.txt`**: List Python dependencies for the backend.
*   **`V1_EOL/mongo-init.js`**: Script for initializing the MongoDB database.

---

## 📊 **DATA FLOW (Conceptual)**

1.  **Configuration (User/Admin):** Trading parameters, API keys, and system settings are provided via the frontend (or environment variables) and stored/managed by `config.py` and potentially MongoDB.
2.  **Frontend Interaction:** The user interacts with `frontend_simple.html` (React application) to view data, create bots, and manage trading operations.
3.  **API Requests (Frontend to Backend):** Frontend sends requests (e.g., start bot, get market data) to `backend/server.py` via HTTP/REST endpoints.
4.  **Backend Processing & Logic:** `backend/server.py` routes requests to appropriate services: 
    *   `engine/` (core trading logic)
    *   `exchange_apis/` (interact with external exchanges)
    *   `risk_management/` (apply risk controls)
    *   `ai_integration/` (send data to/get recommendations from SHENRON)
5.  **Data Storage/Retrieval:** Backend services interact with MongoDB (for persistent data like bot configurations, trade logs) and Redis (for caching real-time data, session management).
6.  **External Exchange Interaction:** `exchange_apis/` communicate with external cryptocurrency exchanges to fetch market data and execute trades.
7.  **Monitoring & Alerts:** `monitoring/` modules collect performance data, `secure_logging.py` logs events, and `ai_integration/shenron_reporter.py` sends critical data to the SHENRON dashboard.
8.  **Real-time Updates (Backend to Frontend):** Frontend receives real-time updates (e.g., market data, bot performance) via WebSockets (if implemented, or through frequent polling of API endpoints).

---

**This document provides a foundational understanding of how ScalpStorm operates, connecting its high-level functions to the specific files and directories that implement them. It should serve as a valuable resource for understanding, debugging, and further developing the platform.**
