"""
Telegram Bot per la Demo "Physio-Concierge".
Permette l'interazione con il sistema tramite Telegram.
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from physio_concierge_demo import rag_pipeline_demo

# Abilita il logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token Bot (da configurare come variabile d'ambiente)
TELEGRAM_TOKEN = "8655617958:AAGWO4Nogj1RuFjEs2DJ6iT0fgfofG3MJMI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start."""
    await update.message.reply_text("Benvenuto! Chiedimi di cercare un fisioterapista.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisci le query utente per il triage attraverso il motore RAG."""
    user_input = ' '.join(context.args)
    if not user_input:
        await update.message.reply_text("Per favore, inviami una query descrittiva. Ad esempio: Cerco fisioterapista neurologico a Padova.")
        return

    await update.message.reply_text("Sto elaborando la tua richiesta, attendi un momento...")
    response = rag_pipeline_demo(user_input)
    await update.message.reply_text(f"Risultato AI: {response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisci le query testuali dell'utente."""
    user_input = update.message.text
    if not user_input:
        return

    await update.message.reply_text("Sto elaborando la tua richiesta, attendi un momento...")
    try:
        response = rag_pipeline_demo(user_input)
        await update.message.reply_text(f"Risultato AI: {response}")
    except Exception as e:
        error_msg = f"Spiacente, si è verificato un errore durante l'elaborazione: {str(e)}"
        print(f"ERROR: {error_msg}")
        await update.message.reply_text(error_msg)

# Configura il bot
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()