# Physio-Concierge Bot 🤖

## Panoramica

**Physio-Concierge** è un bot Telegram intelligente progettato per assistere pazienti nella ricerca di fisioterapisti e nel triage fisioterapico iniziale. Utilizza tecniche di **Retrieval-Augmented Generation (RAG)** per fornire risposte personalizzate e accurate basate su un database di fisioterapisti e linee guida cliniche.

---

## 🎯 Cosa Può Fare il Bot

### 1. **Ricerca Fisioterapisti**
Il bot permette di cercare fisioterapisti in base a:
- **Specializzazione** (es. riabilitazione neurologica, post-operatorio ortopedico)
- **Zona geografica** (es. Padova, Venezia)
- **Disponibilità a domicilio**

**Esempio di interazione:**
```
Utente: "Cerco un fisioterapista neurologico a Padova"
Bot: "Il Dr. Rossi è specializzato in Riabilitazione Neurologica nella zona di Padova ed è disponibile per trattamenti a domicilio."
```

---

### 2. **Triage Fisioterapico Intelligente**
Il sistema fornisce assistenza iniziale per:
- Comprendere la natura del problema (es. dolore acuto, riabilitazione post-intervento)
- Suggerire il tipo di specializzazione più adatta
- Fornire linee guida preliminari (es. "Per dolore acuto post-operatorio, è importante specificare la data dell'intervento")

**Esempio di interazione:**
```
Utente: "Ho dolore post-operatorio alla spalla"
Bot: "Per il dolore post-operatorio ortopedico, ti consiglio la Dr.ssa Bianchi a Venezia. Ricorda di specificare la data dell'intervento per una valutazione più precisa."
```

---

### 3. **Conversazione Naturale**
Il bot supporta **linguaggio naturale** senza bisogno di comandi rigidi. Puoi semplicemente descrivere il tuo problema o esigenza, e il bot elaborerà la risposta utilizzando intelligenza artificiale.

**Esempio:**
```
Utente: "Ciao, ho bisogno di fisioterapia a domicilio per mia nonna"
Bot: "Il Dr. Rossi offre trattamenti a domicilio nella zona di Padova, specializzato in Riabilitazione Neurologica..."
```

---

## 🛠️ Tecnologie Utilizzate

- **Python 3.10** - Linguaggio di programmazione principale
- **python-telegram-bot 20.3** - Framework per l'integrazione Telegram
- **ChromaDB 0.3.26** - Database vettoriale per la ricerca semantica
- **Google Gemini API** - Modello LLM per generazione risposte e embeddings
- **Ollama (Fallback)** - Modelli locali (qwen2.5:7b) come backup se Gemini non è disponibile
- **Docker** - Containerizzazione per deployment facile e portabile

---

## 📋 Comandi Disponibili

| Comando | Descrizione |
|---------|-------------|
| `/start` | Avvia il bot e mostra il messaggio di benvenuto |
| `/search [query]` | Cerca fisioterapisti con una query specifica |
| Messaggio libero | Invia qualsiasi messaggio in linguaggio naturale per ricevere assistenza |

---

## 🚀 Caratteristiche Tecniche

### Architettura RAG (Retrieval-Augmented Generation)
Il bot utilizza una pipeline in due fasi:

1. **Retrieval (Recupero):**
   - Query del database vettoriale ChromaDB
   - Recupero dei documenti più rilevanti (fisioterapisti, linee guida)
   - Utilizzo di embeddings semantici per matching intelligente

2. **Generation (Generazione):**
   - Costruzione di un prompt arricchito con le informazioni recuperate
   - Generazione di una risposta personalizzata usando Gemini AI
   - Fallback automatico a Ollama locale in caso di errori API

### Resilienza e Fallback
- **Fallback multi-livello:** Gemini API → Gemini CLI → Ollama locale
- **Gestione errori robusta:** Il bot continua a funzionare anche in assenza di connettività API
- **Embeddings alternativi:** Fallback da Gemini embeddings a Ollama embeddings

---

## 📊 Database Demo

Il bot include un database di esempio con:

### Fisioterapisti:
- **Dr. Rossi** - Riabilitazione Neurologica, Padova (disponibile a domicilio)
- **Dr.ssa Bianchi** - Post-Operatorio Ortopedico, Venezia

### Linee Guida:
- Gestione dolore acuto post-operatorio
- Valutazione disponibilità per trattamenti domiciliari

*Nota: Il database è estendibile e può essere popolato con dati reali.*

---

## 🔐 Sicurezza

- **Variabili d'ambiente:** Token e API key non sono mai hardcoded nel codice
- **File `.env`:** Gestione sicura delle credenziali (escluso dal version control)
- **Logging strutturato:** Monitoraggio attività senza esporre dati sensibili

---

## 🐳 Deployment Docker

Il bot è containerizzato e può essere eseguito con un singolo comando:

```bash
docker run -d --name physio-bot --env-file .env physio-bot-demo
```

**Vantaggi:**
- Deployment consistente su qualsiasi sistema
- Isolamento delle dipendenze
- Scalabilità orizzontale (multiple istanze se necessario)

---

## 📈 Possibili Estensioni Future

1. **Database Reale:** Integrazione con API di database di fisioterapisti reali
2. **Prenotazioni Online:** Funzionalità di booking integrata
3. **Multilingua:** Supporto per inglese, spagnolo, ecc.
4. **Geolocalizzazione:** Ricerca fisioterapisti nelle vicinanze usando GPS
5. **Analytics:** Dashboard per monitorare query più frequenti e migliorare il servizio
6. **Voice Input:** Supporto comandi vocali via Telegram

---

## 👥 Caso d'Uso Ideale

Questo bot è pensato per:
- **Pazienti:** Che cercano un fisioterapista adatto alle loro esigenze
- **Studi Medici:** Che vogliono automatizzare il primo contatto e il triage
- **Piattaforme Sanitarie:** Come servizio aggiuntivo per guidare i pazienti

---

## 📞 Supporto

Per maggiori informazioni o segnalazione bug, consulta il repository GitHub del progetto.

---

**Sviluppato con ❤️ per migliorare l'accesso alle cure fisioterapiche**
