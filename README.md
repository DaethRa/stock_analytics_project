# 📈 End-to-End AI-Powered Stock Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-2.8.1-blue?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Gemini API](https://img.shields.io/badge/AI-Gemini_Flash-orange?style=for-the-badge)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-blue?style=for-the-badge&logo=tableau&logoColor=white)

## 📌 Project Overview
An automated, end-to-end Data Engineering and Analytics product designed to track major tech stocks (NVDA, AAPL, MSFT, AMD, TSM). The system extracts real-time and historical market data, stores it in a local Data Warehouse, detects statistical price anomalies, and utilizes a **Large Language Model (Gemini AI)** combined with the News API to generate contextual explanations for market volatility. Alerts are delivered directly via Telegram, and data is exposed to a Tableau dashboard for visual analysis.

**📊 Live Dashboard:** [Insert Link to your Tableau Public here]

## 🏗️ System Architecture

```mermaid
graph TD;
    A[Yahoo Finance API] -->|Extract| B(Python ETL Scripts);
    B -->|Load| C[(PostgreSQL DWH)];
    C -->|Trigger| D{Anomaly Detector};
    D -- >3% Change --> E[News API];
    E -->|Context| F[Gemini 2.5 AI];
    F -->|Insight| G[Telegram Bot];
    C -->|Export| H[Tableau Dashboard];
    I((Apache Airflow)) -.->|Orchestrates| B;
    I -.->|Orchestrates| D;
    I -.->|Orchestrates| H;

⚙️ Tech Stack
Language: Python (Pandas, SQLAlchemy, YFinance)
Database: PostgreSQL (Star Schema layout)
Orchestration: Apache Airflow (Standalone via Docker)
Infrastructure: Docker & Docker Compose
AI & APIs: Google Gemini 2.5 Flash, NewsAPI, Telegram Bot API
BI & Visualization: Tableau Public

📁 Repository Structure
code
Text
stock_analytics_project/
├── dags/
│   └── stock_pipeline.py       # Airflow DAGs (Daily & Intraday triggers)
├── src/
│   ├── data/                   # Auto-generated CSVs for Tableau
│   ├── config.py               # DB Connection Engine
│   ├── etl_daily.py            # Batch processing for historical data
│   ├── etl_intraday.py         # Real-time data extraction & anomaly detection
│   ├── ai_agent.py             # LLM RAG pipeline for news analysis
│   ├── telegram_bot.py         # Alerting system
│   └── export_to_csv.py        # Data preparation for Tableau
├── sql/
│   └── init_db.sql             # DDL scripts (Tables, Indexes, Constraints)
├── docker-compose.yml          # Infrastructure setup
└── requirements.txt            # Python dependencies
🚀 How to Run Locally
1. Clone the repository:
code
Bash
git clone https://github.com/yourusername/stock_analytics_project.git
cd stock_analytics_project
2. Setup Environment Variables:
Create a .env file in the root directory and add the following keys:
code
Env
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_db

GEMINI_API_KEY=your_gemini_key
NEWS_API_KEY=your_newsapi_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
3. Launch Infrastructure (Docker):
code
Bash
sudo docker compose up -d
This command will spin up the PostgreSQL database (auto-executing the DDL scripts) and the Apache Airflow container.
4. Activate the Pipeline:
Navigate to http://localhost:8080
Login with standard Airflow credentials (check container logs if auto-generated).
Unpause the DAGs: daily_stock_etl and intraday_anomaly_monitor.
🧠 Core Logic & Features
Idempotent ETL: All SQL inserts use ON CONFLICT DO NOTHING ensuring data integrity even upon DAG restarts.
AI Anomaly Analysis: If intraday price deviates > 3% from the previous close, the pipeline fetches the top 5 recent news articles and prompts Gemini to explain the market behavior in exactly 2 sentences.
Resilient API Calls: Implementation of try-except blocks for the LLM API to gracefully handle 503 Service Unavailable errors during high demand.
📱 Alert Example (Telegram)
🚨 ANOMALY DETECTED: NVDA
📈 Change: -4.5%
🤖 AI Analysis:
NVIDIA's stock dropped following a broader market sell-off in the semiconductor sector. Concerns over potential export restrictions to China have fueled investor uncertainty.
