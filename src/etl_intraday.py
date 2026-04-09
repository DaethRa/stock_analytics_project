import yfinance as yf
from sqlalchemy import text
from config import engine
import logging
from anomaly_logic import detect_anomaly
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_active_tickers_with_close():
    query = """
        SELECT t.ticker, p.close_price 
        FROM stock_analytics.dim_tickers t
        LEFT JOIN stock_analytics.fact_daily_prices p 
        ON t.ticker = p.ticker
        WHERE p.trade_date = (SELECT MAX(trade_date) FROM stock_analytics.fact_daily_prices)
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return {row[0]: float(row[1]) for row in result if row[1] is not None}

def process_intraday():
    tickers_data = get_active_tickers_with_close()
    
    if not tickers_data:
        logging.warning("No daily close prices found.")
        return

    for ticker, prev_close in tickers_data.items():
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.fast_info['lastPrice']
            now_tz = datetime.now(timezone.utc)

            insert_price_query = text("""
                INSERT INTO stock_analytics.fact_intraday_prices 
                (ticker, timestamp_tz, current_price)
                VALUES (:ticker, :timestamp_tz, :current_price)
                ON CONFLICT (ticker, timestamp_tz) DO NOTHING;
            """)
            
            with engine.connect() as conn:
                conn.execute(insert_price_query, {
                    "ticker": ticker,
                    "timestamp_tz": now_tz,
                    "current_price": current_price
                })

            is_anomaly, change_pct = detect_anomaly(ticker, current_price, prev_close, threshold=0.03)

            if is_anomaly:
                logging.warning(f"ANOMALY DETECTED | {ticker} | Change: {change_pct}%")
                insert_anomaly_query = text("""
                    INSERT INTO stock_analytics.fact_anomalies 
                    (ticker, anomaly_timestamp, price_change_pct)
                    VALUES (:ticker, :anomaly_timestamp, :price_change_pct);
                """)
                with engine.connect() as conn:
                    conn.execute(insert_anomaly_query, {
                        "ticker": ticker,
                        "anomaly_timestamp": now_tz,
                        "price_change_pct": change_pct
                    })
            else:
                logging.info(f"{ticker} | Price: {current_price:.2f} | Change: {change_pct}% | Status: NORMAL")

        except Exception as e:
            logging.error(f"Failed to process {ticker}: {e}")

if __name__ == "__main__":
    logging.info("Starting Intraday ETL...")
    process_intraday()
    logging.info("Intraday ETL finished.")