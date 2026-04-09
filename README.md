📈 AI-Powered Stock Intelligence Pipeline
An End-to-End Data Engineering & Analytics solution for monitoring high-volatility tech stocks.

📌 Project Overview
This project is a production-grade analytical ecosystem designed to track and explain market movements of major tech companies (NVDA, AAPL, MSFT, AMD, TSM).

The system doesn't just collect data; it interprets it. By combining statistical anomaly detection with LLM-based RAG (Retrieval-Augmented Generation), it provides instant, news-driven insights into why a stock price is surging or crashing, delivering these insights straight to Telegram.

💡 Key Features
Automated ETL: Daily batch processing of historical data and intraday monitoring via Airflow.

Anomaly Detection: Real-time identification of price deviations (> 3% or statistical Z-score spikes).

AI Insights (RAG): Integration with Gemini 1.5/3 Flash and News API to summarize the reason behind market volatility in 2 concise sentences.

BI Visualization: A comprehensive Tableau dashboard for historical trend analysis and "Anomaly Heatmaps."

Instant Alerting: Telegram bot notifications containing both data (percent change) and context (AI analysis).

🏗️ System Architecture
Фрагмент кода
graph TD;
    subgraph Data_Extraction
    A[Yahoo Finance API] -->|Market Data| B(Python ETL);
    E[News API] -->|Market Context| F[Gemini 1.5/3 Flash AI];
    end

    subgraph Storage_and_Orchestration
    B -->|Load| C[(PostgreSQL DWH)];
    I((Apache Airflow)) -.->|Orchestrates| B;
    I -.->|Triggers| D{Anomaly Detector};
    end

    subgraph Analytics_and_Delivery
    D -- ">3% Change" --> E;
    F -->|Contextual Insight| G[Telegram Bot];
    C -->|Analytical Views| H[Tableau Dashboard];
    end
⚙️ Tech Stack
Language: Python (Pandas, SQLAlchemy, YFinance)

Database: PostgreSQL (Star Schema: fact_daily_prices, dim_tickers, fact_anomalies)

Orchestration: Apache Airflow (Dockerized)

Infrastructure: Docker & Docker Compose

AI & APIs: Google Gemini API, NewsAPI, Telegram Bot API

BI & Visualization: Tableau Public

📁 Repository Structure
Plaintext
stock_analytics_project/
├── dags/
│   └── stock_pipeline.py       # Airflow DAG definitions
├── src/
│   ├── ai_agent.py             # RAG logic: News + Gemini API integration
│   ├── etl_daily.py            # Historical data batch processing
│   ├── etl_intraday.py         # Real-time monitoring & Anomaly detection
│   ├── telegram_bot.py         # Notification service
│   └── config.py               # Centralized configuration & DB engine
├── sql/
│   └── init_db.sql             # Database schema (DDL)
├── docker-compose.yml          # Container orchestration (Airflow, Postgres)
└── requirements.txt            # Project dependencies
🚀 Quick Start (Local Deployment)
1. Clone & Prepare
Bash
git clone https://github.com/yourusername/stock_analytics_project.git
cd stock_analytics_project
2. Environment Setup
Create a .env file in the root directory:

Фрагмент кода
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_DB=stock_db

# External APIs
GEMINI_API_KEY=your_gemini_key
NEWS_API_KEY=your_newsapi_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_id
3. Launch Infrastructure
Bash
# Initialize Airflow (first time only)
docker compose up airflow-init

# Start all services
docker compose up -d
4. Access the Dashboard
Airflow UI: http://localhost:8080 (Default: airflow/airflow)

Database: localhost:5432

Tableau: https://public.tableau.com/views/AI-PoweredStockMarketTracker/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

📱 Alert Example
🚨 ANOMALY DETECTED: NVDA
📈 Change: -4.8%
🤖 AI Analysis:
NVIDIA's stock is experiencing a pullback following reports of new export restrictions on AI chips. Additionally, a broader rotation from tech to value stocks is weighing on the semiconductor sector.
