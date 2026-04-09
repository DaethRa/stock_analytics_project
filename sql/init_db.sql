CREATE SCHEMA IF NOT EXISTS stock_analytics;

CREATE TABLE IF NOT EXISTS stock_analytics.dim_tickers (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    sector VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO stock_analytics.dim_tickers (ticker, company_name, sector)
VALUES 
    ('NVDA', 'NVIDIA Corporation', 'Technology'),
    ('AMD', 'Advanced Micro Devices', 'Technology'),
    ('TSM', 'Taiwan Semiconductor', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    ('AAPL', 'Apple Inc.', 'Technology')
ON CONFLICT (ticker) DO NOTHING;


CREATE TABLE IF NOT EXISTS stock_analytics.fact_daily_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) REFERENCES stock_analytics.dim_tickers(ticker),
    trade_date DATE NOT NULL,
    open_price NUMERIC(10, 4),
    high_price NUMERIC(10, 4),
    low_price NUMERIC(10, 4),
    close_price NUMERIC(10, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_ticker_date UNIQUE (ticker, trade_date)
);

CREATE INDEX idx_daily_ticker_date ON stock_analytics.fact_daily_prices(ticker, trade_date);


CREATE TABLE IF NOT EXISTS stock_analytics.fact_intraday_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) REFERENCES stock_analytics.dim_tickers(ticker),
    timestamp_tz TIMESTAMP WITH TIME ZONE NOT NULL,
    current_price NUMERIC(10, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_ticker_ts UNIQUE (ticker, timestamp_tz)
);

CREATE INDEX idx_intraday_ticker_ts ON stock_analytics.fact_intraday_prices(ticker, timestamp_tz DESC);


CREATE TABLE IF NOT EXISTS stock_analytics.fact_anomalies (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) REFERENCES stock_analytics.dim_tickers(ticker),
    anomaly_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    price_change_pct NUMERIC(5, 2) NOT NULL,
    llm_explanation TEXT,
    is_alert_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_anomalies_ticker_ts ON stock_analytics.fact_anomalies(ticker, anomaly_timestamp DESC);