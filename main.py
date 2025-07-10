import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from bot import start, monitor_risk, button_handler, auto_hedge, stop_auto_hedge, hedge_status

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    TELEGRAM_TOKEN = "8180833255:AAFk88kLaAMNA2FQ958r01Pp_Mto0il7yok"
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.job_queue

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("monitor_risk", monitor_risk))
    app.add_handler(CommandHandler("auto_hedge", auto_hedge))
    app.add_handler(CommandHandler("stop_auto_hedge", stop_auto_hedge))
    app.add_handler(CommandHandler("hedge_status", hedge_status))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
