import yfinance as yf
import pandas as pd
from sqlalchemy import text
from config import engine
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_tickers_from_db():
    """Retrieves a list of tickers from our database"""
    query = "SELECT ticker FROM stock_analytics.dim_tickers;"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        tickers = [row[0] for row in result]
    return tickers

def fetch_and_load_daily_data(tickers):
    """Downloads data from yfinance and loads it into PostgreSQL"""
    
    for ticker in tickers:
        logging.info(f"Downloading data for {ticker}...")
        
        stock = yf.Ticker(ticker)
        df = stock.history(period="7d", interval="1d")
        
        if df.empty:
            logging.warning(f"No data for {ticker}. Skipping.")
            continue
            
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.date 
        
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        df.columns = ['trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
        df['ticker'] = ticker
        
        insert_query = text("""
            INSERT INTO stock_analytics.fact_daily_prices 
            (ticker, trade_date, open_price, high_price, low_price, close_price, volume)
            VALUES (:ticker, :trade_date, :open_price, :high_price, :low_price, :close_price, :volume)
            ON CONFLICT (ticker, trade_date) DO NOTHING;
        """)
        
        records = df.to_dict(orient='records')
        
        with engine.connect() as conn:
            for record in records:
                conn.execute(insert_query, record)
                
        logging.info(f"✅ Data for {ticker} successfully loaded!")

if __name__ == "__main__":
    logging.info("🚀 Launching daily ETL process...")
    try:
        active_tickers = get_tickers_from_db()
        logging.info(f"Found tickers to update: {len(active_tickers)} ({', '.join(active_tickers)})")
        
        fetch_and_load_daily_data(active_tickers)
        logging.info("🏁 ETL process completed successfully!")
        
    except Exception as e:
        logging.error(f"❌ Critical error in ETL: {e}")