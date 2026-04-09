import os
import pandas as pd
from sqlalchemy import text
from config import engine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_data_for_tableau():
    prices_query = "SELECT * FROM stock_analytics.fact_daily_prices ORDER BY trade_date DESC;"
    anomalies_query = "SELECT * FROM stock_analytics.fact_anomalies ORDER BY anomaly_timestamp DESC;"
    
    try:
        with engine.connect() as conn:
            prices_result = conn.execute(text(prices_query))
            prices_df = pd.DataFrame(prices_result.fetchall(), columns=prices_result.keys())
            
            anomalies_result = conn.execute(text(anomalies_query))
            anomalies_df = pd.DataFrame(anomalies_result.fetchall(), columns=anomalies_result.keys())
        
        prices_path = os.path.join(EXPORT_DIR, 'tableau_prices.csv')
        anomalies_path = os.path.join(EXPORT_DIR, 'tableau_anomalies.csv')
        
        prices_df.to_csv(prices_path, index=False)
        anomalies_df.to_csv(anomalies_path, index=False)
        
        logging.info(f"Data successfully exported to {EXPORT_DIR}")
    except Exception as e:
        logging.error(f"Failed to export data: {e}")
        raise e

if __name__ == "__main__":
    logging.info("Starting Data Export...")
    export_data_for_tableau()