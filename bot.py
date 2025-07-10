import ccxt
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from hedge_logic import calculate_optimal_hedge_size, simulate_hedge
from risk_calculations import calculate_spot_delta, calculate_greeks, calculate_var, save_risk_log, generate_var_chart

AUTO_HEDGE_STATUS = {"enabled": False, "strategy": None, "threshold": None}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "/monitor_risk <asset> <position_size> <threshold>\n"
        "/hedge_now <asset> <size> <partial_pct>\n"
        "/auto_hedge <strategy> <threshold>\n"
        "/stop_auto_hedge\n"
        "/hedge_status\n"
        "/hedge_history <asset>\n"
    )

async def monitor_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asset = context.args[0].upper()
    position_size = float(context.args[1])
    threshold = float(context.args[2])

    bybit = ccxt.bybit()
    bybit.load_markets()
    symbol = f"{asset}/USDT"
    ticker = bybit.fetch_ticker(symbol)
    price = ticker["last"]

    delta = calculate_spot_delta(position_size)
    gamma, theta, vega = calculate_greeks(position_size)
    position_value = position_size * price
    var = calculate_var(position_value)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_risk_log(asset, delta, gamma, theta, vega, var, price, timestamp)

    msg = (
        f"*Risk for {asset}*\n\n"
        f"• Size: {position_size}\n"
        f"• Price: ${price:,.2f}\n"
        f"• Delta: {delta}\n"
        f"• VaR: ${var:,.2f}\n"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Hedge Now", callback_data=f"hedgenow_{asset}_{delta}")],
        [InlineKeyboardButton("⚙ Adjust Threshold", callback_data="adjust_threshold")],
        [InlineKeyboardButton("📊 View VaR Chart", callback_data="showchart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if delta > threshold:
        await update.message.reply_text(msg + "\n⚠️ Delta above threshold!", reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(msg + "\n✅ Risk within threshold.", parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("hedgenow"):
        _, asset, delta_str = data.split("_")
        delta_to_hedge = float(delta_str)
        hedge_size = calculate_optimal_hedge_size(delta_to_hedge)

        bybit = ccxt.bybit()
        bybit.load_markets()
        ticker = bybit.fetch_ticker(f"{asset}/USDT")
        price = ticker["last"]

        result = simulate_hedge(asset, hedge_size, est_price=price)
        await query.edit_message_text(result)

    elif data == "adjust_threshold":
        AUTO_HEDGE_STATUS["threshold"] = (AUTO_HEDGE_STATUS["threshold"] or 0) + 100
        await query.edit_message_text(f"New threshold set: {AUTO_HEDGE_STATUS['threshold']}")

    elif data == "showchart":
        chart_file = generate_var_chart()
        if chart_file:
            await query.message.reply_photo(photo=open(chart_file, "rb"))
        else:
            await query.edit_message_text("No historical data available.")

async def auto_hedge_check(context: ContextTypes.DEFAULT_TYPE):
    if not AUTO_HEDGE_STATUS["enabled"]:
        return

    asset = "BTC"
    position_size = 1.5
    threshold = AUTO_HEDGE_STATUS["threshold"]

    bybit = ccxt.bybit()
    bybit.load_markets()
    ticker = bybit.fetch_ticker(f"{asset}/USDT")
    price = ticker["last"]

    delta = calculate_spot_delta(position_size)

    if delta > threshold:
        hedge_size = calculate_optimal_hedge_size(delta)
        result = simulate_hedge(asset, hedge_size, est_price=price)
        await context.bot.send_message(chat_id=context.job.chat_id, text=f"⚠️ Auto hedge triggered!\n\n{result}")

async def auto_hedge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    strategy = context.args[0]
    threshold = float(context.args[1])
    AUTO_HEDGE_STATUS["enabled"] = True
    AUTO_HEDGE_STATUS["strategy"] = strategy
    AUTO_HEDGE_STATUS["threshold"] = threshold

    job_queue = context.application.job_queue
    chat_id = update.effective_chat.id

    for job in job_queue.get_jobs_by_name("auto_hedge_job"):
        job.schedule_removal()


    job_queue.run_repeating(auto_hedge_check, interval=60, first=5, chat_id=chat_id, name="auto_hedge_job")

    await update.message.reply_text(f"✅Auto hedge enabled.\nStrategy: {strategy}\nThreshold: {threshold}\nChecking every 60 sec.")

async def stop_auto_hedge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    AUTO_HEDGE_STATUS["enabled"] = False
    job_queue = context.application.job_queue

    for job in job_queue.get_jobs_by_name("auto_hedge_job"):
        job.schedule_removal()

    await update.message.reply_text("⛔Auto hedge stopped.")


async def hedge_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "Enabled" if AUTO_HEDGE_STATUS["enabled"] else "Disabled"
    strategy = AUTO_HEDGE_STATUS["strategy"]
    threshold = AUTO_HEDGE_STATUS["threshold"]
    await update.message.reply_text(f"Status: {status}\nStrategy: {strategy}\nThreshold: {threshold}")
