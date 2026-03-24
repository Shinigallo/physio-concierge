"""
Demo Funzionante per "Physio-Concierge" utilizzando il modello locale Qwen3.5
"""

import chromadb
from chromadb.config import Settings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import subprocess

import requests
import json

# Configurazione Ollama (Host accessibile dal container)
OLLAMA_URL = "http://172.17.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen3.5:9b"

def run_local_model(prompt):
    """Esegue il modello tramite Ollama API."""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Errore nell'esecuzione di Ollama: {str(e)}"

# Dati d'esempio pre-caricati
fisioterapisti = [
    {"nome": "Dr. Rossi", "specializzazione": "Riabilitazione Neurologica", "zona": "Padova", "disponibile_domicilio": True},
    {"nome": "Dr.ssa Bianchi", "specializzazione": "Post-Operatorio Ortopedico", "zona": "Venezia", "disponibile_domicilio": False},
]

linee_guida = [
    "Per dolore acuto post-operatorio, richiedere data dell'intervento.",
    "Valutare disponibilità del terapista per il trattamento domiciliare."
]

# Configurazione ChromaDB
def setup_chroma():
    """Configura ed inizializza il database vettoriale per demo."""
    chroma_client = chromadb.Client(Settings(
        persist_directory="./chroma_demo",
        anonymized_telemetry=False
    ))
    collection = chroma_client.get_or_create_collection(name="demo_fisioterapisti")

    for fisioterapista in fisioterapisti:
        testo = f"{fisioterapista['nome']} - {fisioterapista['specializzazione']} - {fisioterapista['zona']}"
        collection.add(
            documents=[testo],
            metadatas=[fisioterapista],
            ids=[fisioterapista['nome']]
        )

    for i, linea in enumerate(linee_guida):
        collection.add(documents=[linea], ids=[f"linea-{i}"])

    return collection

# Pipeline con Qwen3.5
def rag_pipeline_demo(query):
    """Pipeline demo per il triage fisioterapico."""
    collection = setup_chroma()
    risultati = collection.query(query_texts=[query], n_results=2)
    # ChromaDB restituisce una lista di liste per 'documents'
    risultati_testo = "\n".join(risultati['documents'][0])

    prompt = f"""
    Domanda: {query}
    Informazioni Recuperate: {risultati_testo}

    In base ai risultati ottenuti, genera una risposta dettagliata ma concisa per il paziente.
    """

    return run_local_model(prompt)

# Esecuzione della Demo
if __name__ == "__main__":
    query = "Cerco un fisioterapista a domicilio per riabilitazione neurologica a Padova."
    risposta = rag_pipeline_demo(query)
    print("Risposta AI:", risposta)