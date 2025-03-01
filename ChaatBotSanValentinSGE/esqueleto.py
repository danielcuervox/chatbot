from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from diccionarioAUtilizar import personas


TOKEN = "8094790083:AAG3avVXNxsjeLWbklMYy2fJoDwgKRB1qrQ"

# ------------------------------- métodos -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
       # reply_markup=ForceReply(selective=True),
    )


# ------------------------------- main -------------------------------

def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))


    app.run_polling()

if __name__ == "__main__":
    main()