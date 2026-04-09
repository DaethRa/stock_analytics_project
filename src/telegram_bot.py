import os
import requests
import html
from sqlalchemy import text
from config import engine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID", "")).strip()

def send_message(message_text):
    if not BOT_TOKEN or not CHAT_ID:
        logging.error("Telegram credentials missing.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"Telegram API Error: {response.text}")
            return False
        return True
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")
        return False

def process_alerts():
    query = """
        SELECT id, ticker, price_change_pct, llm_explanation 
        FROM stock_analytics.fact_anomalies 
        WHERE llm_explanation IS NOT NULL 
        AND is_alert_sent = FALSE
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            anomalies = [dict(row._mapping) for row in result]
            
            if not anomalies:
                logging.info("No new alerts to send.")
                return

            for anomaly in anomalies:
                safe_explanation = html.escape(str(anomaly['llm_explanation']))
                
                msg = (
                    f"🚨 <b>ANOMALY DETECTED: {anomaly['ticker']}</b>\n\n"
                    f"📈 <b>Change:</b> {anomaly['price_change_pct']}%\n\n"
                    f"🤖 <b>AI Analysis:</b>\n{safe_explanation}"
                )
                
                if send_message(msg):
                    update_query = text("""
                        UPDATE stock_analytics.fact_anomalies 
                        SET is_alert_sent = TRUE 
                        WHERE id = :id
                    """)
                    conn.execute(update_query, {"id": anomaly['id']})
                    logging.info(f"Alert sent for {anomaly['ticker']}.")
    except Exception as e:
        logging.error(f"Database error during alert processing: {e}")

if __name__ == "__main__":
    logging.info("Starting Telegram Alert Pipeline...")
    process_alerts()
    logging.info("Telegram Alert Pipeline finished.")