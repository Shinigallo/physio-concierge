"""
Prototipo AI "Physio-Concierge" con Architettura RAG per Tecnobe srl.
Author: Assistant
Descrizione: Questo script Python dimostra come usare ChromaDB e LangChain per costruire un motore RAG
per il triage fisioterapico, con compliance GDPR e scrubbing dei dati.
"""

import chromadb
from chromadb.config import Settings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Dati d'esempio: fisioterapisti e linee guida
fisioterapisti = [
    {"nome": "Dr. Rossi", "specializzazione": "Riabilitazione Neurologica", "zona": "Padova", "disponibile_domicilio": True},
    {"nome": "Dr.ssa Bianchi", "specializzazione": "Post-Operatorio Ortopedico", "zona": "Venezia", "disponibile_domicilio": False},
    {"nome": "Dr. Verdi", "specializzazione": "Terapia del Dolore", "zona": "Treviso", "disponibile_domicilio": True},
]

linee_guida = [
    "Per dolore acuto post-operatorio, richiedere data dell'intervento.",
    "I pazienti neurologici devono essere valutati per segni di spasticità.",
    "Valutare disponibilità del terapista per il trattamento domiciliare, se necessario."
]

# Funzione per creare un Vector Database con ChromaDB
def setup_chroma():
    """Configura il database vettoriale con i dati d'esempio."""
    chroma_client = chromadb.Client(Settings(
        persist_directory="./chroma_data",
        anonymized_telemetry=False
    ))
    collection = chroma_client.get_or_create_collection(name="fisioterapisti")

    # Caricamento dei fisioterapisti come documenti
    for fisioterapista in fisioterapisti:
        testo = f"{fisioterapista['nome']} - {fisioterapista['specializzazione']} - {fisioterapista['zona']}"
        collection.add(
            documents=[testo],
            metadatas=[fisioterapista],
            ids=[fisioterapista['nome']]
        )

    # Caricamento delle linee guida come documenti
    for i, linea in enumerate(linee_guida):
        collection.add(documents=[linea], ids=[f"linea-{i}"])

    return collection

# Data Scrubbing con modello locale (esempio semplificato)
# In produzione, sostituire con una chiamata reale al modello Ollama.
def data_scrubbing(input_text):
    """Simula la rimozione di dati sensibili (es: nomi pazienti)."""
    return input_text.replace("nonno", "[DATI RIMOSSI]")

# Funzione principale per la pipeline RAG
def rag_pipeline(query):
    """Gestisce la pipeline RAG: ricerca semantica e generazione risposta."""

    # Pulizia dei dati utente
    query_cleaned = data_scrubbing(query)

    # Recupero dal Vector DB
    collection = setup_chroma()
    risultati = collection.query(query_texts=[query_cleaned], n_results=2)

    # LLM: Generazione di risposta con il contesto recuperato
    llm = OpenAI(temperature=0.7, model_name="gpt-4")  # API GPT-4
    prompt = PromptTemplate(
        input_variables=["query", "results"],
        template="""
        Domanda: {query}
        Informazioni Recuperate: {results}

        Genera una raccomandazione personalizzata per il paziente basata sulle informazioni sopra.
        """
    )

    chain = RetrievalQA(retriever=None, llm=llm)
    return chain.run({"query": query, "results": risultati})

# Esecuzione d'esempio
if __name__ == "__main__":
    domanda = "Cerco un esperto per mio nonno che ha avuto un ictus."
    risposta = rag_pipeline(domanda)
    print("Risultato Finalizzato:", risposta)
