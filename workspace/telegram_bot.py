"""
Telegram Bot per la Demo "Physio-Concierge".
Permette l'interazione con il sistema di triage fisioterapico tramite Telegram.

Il bot gestisce sia comandi specifici (/start, /search) che messaggi naturali,
permettendo agli utenti di cercare fisioterapisti e ricevere assistenza in linguaggio naturale.
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from physio_concierge_demo import rag_pipeline_demo

# ==================== CONFIGURAZIONE ====================

# Abilita logging per debug e monitoraggio
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token del bot Telegram (caricato da variabile d'ambiente per sicurezza)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN non è impostata nelle variabili d'ambiente.")

# ==================== HANDLER COMANDI ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestisce il comando /start.
    Invia un messaggio di benvenuto all'utente.
    """
    await update.message.reply_text(
        "👋 Benvenuto nel sistema Physio-Concierge!\n\n"
        "Puoi chiedermi informazioni sui fisioterapisti disponibili, "
        "cercare specializzazioni specifiche o richiedere assistenza per il triage fisioterapico.\n\n"
        "Esempio: 'Cerco un fisioterapista neurologico a Padova'"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestisce il comando /search seguito da una query.
    Esempio: /search fisioterapista neurologico Padova
    
    Args:
        update: Oggetto Update di python-telegram-bot
        context: Contesto contenente gli argomenti del comando
    """
    # Estrai la query dagli argomenti del comando
    user_input = ' '.join(context.args)
    
    if not user_input:
        await update.message.reply_text(
            "⚠️ Per favore, specifica cosa cerchi.\n\n"
            "Esempio: /search fisioterapista neurologico a Padova"
        )
        return

    # Notifica all'utente che la richiesta è in elaborazione
    await update.message.reply_text("🔍 Sto elaborando la tua richiesta, attendi un momento...")
    
    # Esegui la pipeline RAG per generare la risposta
    response = rag_pipeline_demo(user_input)
    await update.message.reply_text(f"📋 Risultato:\n\n{response}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestisce i messaggi testuali naturali inviati dall'utente.
    Permette conversazione senza bisogno di comandi specifici.
    
    Questa funzione processa qualsiasi messaggio di testo che non è un comando,
    permettendo all'utente di interagire in modo naturale con il bot.
    
    Args:
        update: Oggetto Update di python-telegram-bot
        context: Contesto della conversazione
    """
    user_input = update.message.text
    
    # Ignora messaggi vuoti
    if not user_input:
        return

    # Notifica all'utente che la richiesta è in elaborazione
    await update.message.reply_text("🔍 Sto elaborando la tua richiesta, attendi un momento...")
    
    try:
        # Esegui la pipeline RAG per generare la risposta
        response = rag_pipeline_demo(user_input)
        await update.message.reply_text(f"📋 Risultato:\n\n{response}")
    except Exception as e:
        # Gestione errori: notifica all'utente e logga l'errore
        error_msg = f"⚠️ Spiacente, si è verificato un errore durante l'elaborazione."
        logging.error(f"Errore durante l'elaborazione della richiesta: {str(e)}")
        await update.message.reply_text(error_msg)


# ==================== MAIN ====================

def main():
    """
    Funzione principale che configura e avvia il bot Telegram.
    
    Configura:
    - Application builder con il token del bot
    - Handler per comandi (/start, /search)
    - Handler per messaggi testuali generici
    - Polling loop per ricevere gli aggiornamenti
    """
    # Inizializza l'applicazione Telegram
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Registra gli handler per i comandi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    
    # Registra l'handler per messaggi testuali (esclusi i comandi)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Avvia il polling per ricevere gli aggiornamenti
    logging.info("🤖 Bot avviato. In attesa di messaggi...")
    application.run_polling()


if __name__ == "__main__":
    main()
