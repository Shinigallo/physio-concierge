"""
Demo Funzionante per "Physio-Concierge" utilizzando Gemini API e fallback Ollama.

Questo modulo implementa una pipeline RAG (Retrieval-Augmented Generation) per un sistema
di triage fisioterapico. Il sistema recupera informazioni da un database vettoriale (ChromaDB)
e genera risposte personalizzate usando modelli LLM (Gemini o Ollama come fallback).
"""

import chromadb
import os
import json
import subprocess
from chromadb.config import Settings
import google.generativeai as genai

# ==================== CONFIGURAZIONE ====================

# Configurazione Gemini API tramite variabile d'ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY non è impostata nelle variabili d'ambiente.")
genai.configure(api_key=GEMINI_API_KEY)

# ==================== DATI DI ESEMPIO ====================

# Database fisioterapisti per la demo
fisioterapisti = [
    {
        "nome": "Dr. Rossi",
        "specializzazione": "Riabilitazione Neurologica",
        "zona": "Padova",
        "disponibile_domicilio": True
    },
    {
        "nome": "Dr.ssa Bianchi",
        "specializzazione": "Post-Operatorio Ortopedico",
        "zona": "Venezia",
        "disponibile_domicilio": False
    },
]

# Linee guida per il triage
linee_guida = [
    "Per dolore acuto post-operatorio, richiedere data dell'intervento.",
    "Valutare disponibilità del terapista per il trattamento domiciliare."
]

# ==================== FUNZIONI CORE ====================

def run_local_model(prompt):
    """
    Esegue il modello Gemini per generare una risposta al prompt fornito.
    In caso di errore, tenta un fallback tramite Gemini CLI e poi Ollama locale.
    
    Args:
        prompt (str): Il prompt da inviare al modello.
        
    Returns:
        str: La risposta generata dal modello.
    """
    print(f"DEBUG: Inviando richiesta a Gemini (gemini-flash-latest)...")
    try:
        # Tentativo con libreria ufficiale Gemini
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        print(f"DEBUG: Risposta ricevuta da Gemini.")
        return response.text.strip()
    except Exception as e:
        print(f"DEBUG: Errore Gemini API: {str(e)}")
        
        # Fallback 1: Gemini CLI
        try:
            escaped_prompt = prompt.replace('"', '\\"')
            cmd = f'gemini -p "{escaped_prompt}"'
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as cli_error:
            print(f"DEBUG: Fallback Gemini CLI fallito: {str(cli_error)}")
        
        # Fallback 2: Ollama locale
        try:
            print("DEBUG: Tentativo fallback con Ollama locale (qwen2.5:7b)...")
            result = subprocess.run(
                ['docker', 'exec', 'ollama', 'ollama', 'run', 'qwen2.5:7b', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as ollama_error:
            print(f"DEBUG: Fallback Ollama fallito: {str(ollama_error)}")
        
        return f"Errore: impossibile generare risposta. Dettagli: {str(e)}"


def gemini_embedding_fn(input: list) -> list:
    """
    Genera embeddings vettoriali per il testo fornito usando Gemini Embedding API.
    In caso di errore, usa Ollama locale come fallback.
    
    Args:
        input (list): Lista di stringhe da convertire in embeddings.
        
    Returns:
        list: Lista di vettori di embedding.
    """
    try:
        # Tentativo con Gemini Embedding API
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=input,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"DEBUG: Errore Embedding Gemini: {str(e)}")
        
        # Fallback: Ollama locale con modello qwen2.5:7b
        try:
            print("DEBUG: Fallback embedding con Ollama locale...")
            result = subprocess.run(
                ['docker', 'exec', 'ollama', 'ollama', 'run', 'qwen2.5:7b', '--embedding', json.dumps(input)],
                capture_output=True,
                text=True,
                timeout=30
            )
            return json.loads(result.stdout)
        except Exception as ollama_error:
            print(f"DEBUG: Fallback embedding Ollama fallito: {str(ollama_error)}")
            # Fallback finale: vettore zero (768 dimensioni compatibile con all-MiniLM-L6-v2)
            return [[0.0] * 768] * len(input)


# Cache globale per evitare re-inizializzazioni
_collection_cache = None

def setup_chroma():
    """
    Configura e inizializza il database vettoriale ChromaDB per la demo.
    Carica i dati di fisioterapisti e linee guida se la collezione è vuota.
    
    Returns:
        chromadb.Collection: La collezione ChromaDB inizializzata.
    """
    global _collection_cache
    if _collection_cache is not None:
        return _collection_cache

    # Disabilita telemetria anonima
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    
    # Inizializza client ChromaDB con persistenza locale
    chroma_client = chromadb.Client(Settings(
        persist_directory="./chroma_demo",
        anonymized_telemetry=False
    ))
    
    # Crea o recupera collezione usando la funzione di embedding custom
    collection = chroma_client.get_or_create_collection(
        name="demo_fisioterapisti",
        embedding_function=gemini_embedding_fn
    )

    # Indicizza i dati solo se la collezione è vuota
    if collection.count() == 0:
        print("DEBUG: Indicizzazione dati iniziale...")
        
        # Indicizza fisioterapisti
        for fisioterapista in fisioterapisti:
            testo = f"{fisioterapista['nome']} - {fisioterapista['specializzazione']} - {fisioterapista['zona']}"
            collection.add(
                documents=[testo],
                metadatas=[fisioterapista],
                ids=[fisioterapista['nome']]
            )

        # Indicizza linee guida
        for i, linea in enumerate(linee_guida):
            collection.add(
                documents=[linea],
                ids=[f"linea-{i}"]
            )
    
    _collection_cache = collection
    return collection


def rag_pipeline_demo(query):
    """
    Pipeline RAG (Retrieval-Augmented Generation) per il triage fisioterapico.
    
    Flusso:
    1. Recupera documenti rilevanti dal database vettoriale ChromaDB
    2. Costruisce un prompt arricchito con le informazioni recuperate
    3. Genera una risposta usando Gemini (o Ollama come fallback)
    
    Args:
        query (str): La domanda o richiesta dell'utente.
        
    Returns:
        str: La risposta generata dal sistema.
    """
    # Inizializza ChromaDB
    collection = setup_chroma()
    
    # Query il database vettoriale per recuperare i documenti più rilevanti
    risultati = collection.query(query_texts=[query], n_results=2)
    
    # Estrai i documenti recuperati (ChromaDB 0.3.x restituisce liste annidate)
    if risultati['documents'] and len(risultati['documents']) > 0:
        risultati_testo = "\n".join(risultati['documents'][0])
    else:
        risultati_testo = "Nessuna informazione specifica trovata."

    # Costruisci il prompt per il modello LLM
    prompt = f"""
    Domanda: {query}
    Informazioni Recuperate: {risultati_testo}

    In base ai risultati ottenuti, genera una risposta dettagliata ma concisa per il paziente.
    Rispondi in modo professionale come un assistente di triage fisioterapico.
    """

    # Genera e restituisci la risposta
    return run_local_model(prompt)


# ==================== ESECUZIONE DIRETTA ====================

if __name__ == "__main__":
    # Test della pipeline con una query di esempio
    query = "Cerco un fisioterapista a domicilio per riabilitazione neurologica a Padova."
    risposta = rag_pipeline_demo(query)
    print("Risposta AI:", risposta)
