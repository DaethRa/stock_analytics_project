import os
import requests
from google import genai
from sqlalchemy import text
from config import engine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_unprocessed_anomalies():
    query = """
        SELECT id, ticker, anomaly_timestamp, price_change_pct 
        FROM stock_analytics.fact_anomalies 
        WHERE llm_explanation IS NULL
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]

def fetch_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return "\n".join([f"- {a['title']}: {a['description']}" for a in articles if a['title']])
    return ""

def generate_explanation(ticker, change_pct, news_text):
    if not news_text:
        return "No recent news found to explain the anomaly."
    
    prompt = f"You are a senior financial analyst. The stock {ticker} changed by {change_pct}%. Based on the following news, explain why. Be concise, max 2 sentences.\n\nNews:\n{news_text}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        logging.error(f"LLM API Error: {e}")
        return "Failed to generate explanation due to LLM API error."

def update_anomaly_explanation(anomaly_id, explanation):
    query = text("""
        UPDATE stock_analytics.fact_anomalies 
        SET llm_explanation = :explanation 
        WHERE id = :id
    """)
    with engine.connect() as conn:
        conn.execute(query, {"explanation": explanation, "id": anomaly_id})

def process_anomalies():
    anomalies = get_unprocessed_anomalies()
    if not anomalies:
        logging.info("No new anomalies to process.")
        return

    for anomaly in anomalies:
        logging.info(f"Processing anomaly for {anomaly['ticker']}")
        news = fetch_news(anomaly['ticker'])
        explanation = generate_explanation(anomaly['ticker'], anomaly['price_change_pct'], news)
        update_anomaly_explanation(anomaly['id'], explanation)
        logging.info(f"Explanation for {anomaly['ticker']} saved to DB.")

if __name__ == "__main__":
    logging.info("Starting AI Agent Pipeline...")
    process_anomalies()
    logging.info("AI Agent Pipeline finished.")