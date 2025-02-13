import logging

from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    logger.info(update.message.text)
    await update.message.reply_text(update.message.text)



async def menu(update: Update, context: CallbackContext) -> None:
    """Send a menu."""
    keyboardOpciones = [["Moto", "Coche"]]
    reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)

    await update.message.reply_text("Elige tu opción de consulta:", reply_markup=reply_markup)

async def option_selected(update: Update, context: CallbackContext) -> None:
    """segunda opciones árbol"""
    text = update.message.text
    keyboardOpciones = []
    print(text)

    if text == "Moto":
        keyboardOpciones = [["<50cc", ">50cc"]]
    elif text == "Coche":
        keyboardOpciones = [["<50cc", ">50cc"]]

    reply_markup = ReplyKeyboardMarkup(keyboardOpciones, resize_keyboard=True, one_time_keyboard=True, selective=True)
    await update.message.reply_text("Elige tu opción de consulta:", reply_markup=reply_markup)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("8094790083:AAG3avVXNxsjeLWbklMYy2fJoDwgKRB1qrQ").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    application.add_handler(CommandHandler("contratar", menu))


if __name__ == "__main__":
    main()