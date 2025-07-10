# 📄 **Documentation: Spot Exposure Hedging Bot**

### By: Keerti Madhuvantika A

---

## **Project Overview**

This bot monitors crypto spot positions and allows users to simulate hedging actions directly via Telegram. It is built in Python using the `ccxt` library to fetch real-time exchange data, and Matplotlib to visualize risk metrics.

---

## **File Structure**

- **main.py** — Initializes and starts the Telegram bot; sets up command handlers.
- **bot.py** — Contains logic for Telegram commands and button callbacks.
- **hedge_logic.py** — Contains hedge size calculation and simulation.
- **risk_calculations.py** — Implements risk metrics calculations (delta, Greeks, VaR) and generates historical risk charts.

---

## **Commands & Example Usage**

### `/start`
Displays a welcome message and lists all available commands for quick reference.

### `/monitor_risk BTC 1 0.5`
Monitors a 1 BTC spot position with a delta threshold of 0.5. Shows current price, delta, gamma, theta, vega, and VaR. Provides interactive buttons to hedge immediately, adjust threshold, or view a VaR chart.

### `/auto_hedge simple 0.5`
Enables automatic hedging with strategy "simple" and delta threshold 0.5. The bot continuously monitors the position every 60 seconds and automatically simulates a hedge if the delta exceeds the threshold. You will receive real-time alerts and a detailed cost breakdown whenever an auto hedge is triggered.

### `/stop_auto_hedge`
Stops the auto-hedging feature immediately.

### `/hedge_status`
Displays the current status of auto-hedging, including whether it’s enabled, the selected strategy, and the threshold value.

---

## **Why use a virtual environment?**

Using a virtual environment ensures all dependencies are isolated to this project. This prevents version conflicts with other Python projects on your system, keeps your environment clean, and makes it easier to deploy or share your code.

---

## **Conclusion**

This bot allows for simple, clear, and effective risk monitoring and hedging, all through an interactive Telegram interface. By integrating automated checks and providing detailed feedback, it empowers users to manage their crypto exposure efficiently and confidently.

---

