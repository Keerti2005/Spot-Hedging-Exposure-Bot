import os
import json
import matplotlib.pyplot as plt

HISTORICAL_LOG_FILE = "risk_history.json"

def calculate_spot_delta(position_size):
    return position_size

def calculate_greeks(position_size):
    gamma = 0.01 * position_size
    theta = -0.005 * position_size
    vega = 0.02 * position_size
    return gamma, theta, vega

def calculate_var(position_value, daily_volatility_pct=0.05, confidence=1.65):
    return confidence * daily_volatility_pct * position_value

def save_risk_log(asset, delta, gamma, theta, vega, var, price, timestamp):
    entry = {
        "asset": asset,
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "var": var,
        "price": price,
        "timestamp": timestamp
    }
    if os.path.exists(HISTORICAL_LOG_FILE):
        with open(HISTORICAL_LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(HISTORICAL_LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_var_chart():
    if not os.path.exists(HISTORICAL_LOG_FILE):
        return None
    with open(HISTORICAL_LOG_FILE, "r") as f:
        data = json.load(f)
    times = [entry["timestamp"] for entry in data]
    vars_ = [entry["var"] for entry in data]
    plt.figure(figsize=(10, 5))
    plt.plot(times, vars_, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Timestamp")
    plt.ylabel("VaR ($)")
    plt.title("VaR Over Time")
    plt.tight_layout()
    chart_file = "var_chart.png"
    plt.savefig(chart_file)
    plt.close()
    return chart_file
