def detect_anomaly(ticker, current_price, previous_close, threshold=0.03):
    if not previous_close or previous_close <= 0:
        return False, 0.0
    
    change_pct = ((current_price - previous_close) / previous_close) * 100.0
    is_anomaly = abs(change_pct) >= (threshold * 100)

    
    return is_anomaly, round(change_pct, 2)