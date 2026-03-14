![Pipeline Status](https://github.com/nehaprasad1/financial-ingestion/actions/workflows/main_ingestion.yml/badge.svg)
# Financial Data Pipeline

An automated, cloud-native ETL pipeline designed to ingest, validate, and store real-time stock market data. This project demonstrates a production-ready approach to handling financial time-series data using a modern MLOps stack.

## Professional Highlights
* **Automated CI/CD Orchestration:** Leverages **GitHub Actions** for event-driven data ingestion and deployment.
* **Scalable Storage:** Implements **MongoDB Atlas Time-Series** collections, optimized for high-performance temporal queries and data retention.
* **Robust Data Validation:** Utilizes **Pydantic** to enforce strict schema compliance and ensure data integrity at the ingestion layer.
* **Cloud Security:** Integrated with encrypted **Secret Management** to handle sensitive API credentials and database connection strings.
* **Fault-Tolerant Design:** Engineered with custom retry logic and session management to handle transient networking issues and API rate limits.

## Technical Stack
* **Languages:** Python 3.10+
* **Database:** MongoDB Atlas (Time-Series)
* **Orchestration:** GitHub Actions
* **Libraries:** Pydantic v2, PyYAML, Requests, Dotenv

##  System Architecture
* **`src/main.py`**: The central orchestrator supporting both long-running loops and ephemeral cloud execution.
* **`src/ingestion.py`**: Modular API client with built-in rate-limit handling and connection resilience.
* **`src/models.py`**: Strict Pydantic schemas defining the financial data contract.
* **`src/database.py`**: Automated database initialization and time-series metadata configuration.
* **`config/`**: Decoupled environment configuration for easy asset scaling.

##  Deployment & Automation
The pipeline is fully automated and deployed via GitHub Actions. It supports:
1. **Event-Driven Runs:** Triggered automatically on code pushes to the main branch.
2. **On-Demand Execution:** Manual triggers via GitHub UI for real-time data fetching.
3. **Optimized Runners:** Utilizes dependency caching to minimize deployment latency and compute resource usage.

## Installation & Setup
1. **Clone the repo:** `git clone <your-repository-url>`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Environment:** Add `MONGO_URI` and `ALPHA_VANTAGE_API_KEY` to your secrets.
4. **Execute:** `python src/main.py --once`
