# Physio-Concierge Demo 🤖

Questo progetto è una demo di un **assistente virtuale di triage fisioterapico**, accessibile tramite Telegram, che sfrutta tecniche di **Retrieval-Augmented Generation (RAG)** e i modelli generativi di Google Gemini.

L'obiettivo è quello di comprendere le richieste in linguaggio naturale degli utenti (es. pazienti che cercano un fisioterapista specializzato in una certa zona) e di consultare un database vettoriale (ChromaDB) precaricato con informazioni su vari professionisti e linee guida per elaborare una risposta pertinente e professionale.

## Componenti Principali

- `physio_concierge_demo.py`: Contiene il core logico dell'applicazione, la configurazione di ChromaDB (con embeddings Gemini) e la pipeline RAG che interroga Gemini (`gemini-flash-latest`).
- `telegram_bot.py`: Interfaccia Telegram. Utilizza `python-telegram-bot` per ascoltare le richieste degli utenti e rispondere tramite l'elaborazione RAG in background.
- `Dockerfile` / `Dockerfile-telegram`: File per creare i container Docker per una facile distribuzione dell'applicazione e del bot Telegram isolato.
- `requirements.txt`: Elenco delle dipendenze di Python (es. `chromadb`, `langchain`, `google-generativeai`).

## Come Avviare il Bot (Docker)

Assicurati di aver configurato le API keys (es. `TELEGRAM_TOKEN` e `GEMINI_API_KEY`) all'interno degli script.

```bash
# 1. Build dell'immagine Docker
docker build -t physio-bot-demo -f Dockerfile-telegram .

# 2. Esecuzione del container in background
docker run --rm -d --name physio-bot physio-bot-demo
```

## Esecuzione Locale (Senza Docker)

1. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
2. Assicurati di avere `Node.js` e la CLI di Gemini (`@google/gemini-cli`) qualora si volesse usare il fallback CLI, e configura le API key.
3. Esegui il bot:
   ```bash
   python telegram_bot.py
   ```

## Demo Dati
Attualmente il sistema è popolato con un dataset di prova:
- **Dr. Rossi**: Riabilitazione Neurologica a Padova (disponibile a domicilio).
- **Dr.ssa Bianchi**: Post-Operatorio Ortopedico a Venezia.

Puoi chiedere al bot ad esempio:
- *"Cerco un fisioterapista a domicilio per riabilitazione neurologica a Padova."*
- *"Chi è il Dr. Rossi?"*
- *"Ho un dolore post-operatorio ortopedico, a chi posso rivolgermi?"*
