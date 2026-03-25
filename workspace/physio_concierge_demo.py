"""
Demo Funzionante per "Physio-Concierge" utilizzando il modello locale Qwen3.5
"""

import chromadb
import os
from chromadb.config import Settings
import subprocess
import google.generativeai as genai

# Configurazione Gemini API tramite variabile d'ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY non è impostata nelle variabili d'ambiente.")
genai.configure(api_key=GEMINI_API_KEY)

def run_local_model(prompt):
    """Esegue il modello Gemini tramite libreria ufficiale."""
    print(f"DEBUG: Inviando richiesta a Gemini (gemini-1.5-flash)...")
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        print(f"DEBUG: Risposta ricevuta da Gemini.")
        return response.text.strip()
    except Exception as e:
        print(f"DEBUG: Errore Gemini API: {str(e)}")
        # Fallback a CLI se la libreria fallisce
        try:
            escaped_prompt = prompt.replace('"', '\\"')
            cmd = f'gemini -p "{escaped_prompt}"'
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            return result.stdout.strip()
        except:
            return f"Errore nell'esecuzione di Gemini: {str(e)}"

# Dati d'esempio pre-caricati
fisioterapisti = [
    {"nome": "Dr. Rossi", "specializzazione": "Riabilitazione Neurologica", "zona": "Padova", "disponibile_domicilio": True},
    {"nome": "Dr.ssa Bianchi", "specializzazione": "Post-Operatorio Ortopedico", "zona": "Venezia", "disponibile_domicilio": False},
]

linee_guida = [
    "Per dolore acuto post-operatorio, richiedere data dell'intervento.",
    "Valutare disponibilità del terapista per il trattamento domiciliare."
]

# Cache per la collezione Chroma
_collection_cache = None

# Custom Embedding Function usando Gemini (compatibile con ChromaDB 0.3.x)
def gemini_embedding_fn(input: list) -> list:
    try:
        # Gemini embedding-001
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=input,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"DEBUG: Errore Embedding Gemini: {str(e)}")
        # Fallback embedding (768 zeri per all-MiniLM-L6-v2 compatible size)
        result = subprocess.run(['ollama', 'run', 'qwen2.5:7b', '--embedding', json.dumps(input)], capture_output=True, text=True).stdout
        return json.loads(result)

# Configurazione ChromaDB
def setup_chroma():
    """Configura ed inizializza il database vettoriale per demo."""
    global _collection_cache
    if _collection_cache is not None:
        return _collection_cache

    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    chroma_client = chromadb.Client(Settings(
        persist_directory="./chroma_demo",
        anonymized_telemetry=False
    ))
    
    # Usa la funzione di embedding di Gemini per evitare il download ONNX
    collection = chroma_client.get_or_create_collection(
        name="demo_fisioterapisti",
        embedding_function=gemini_embedding_fn
    )

    # Aggiungi i dati solo se la collezione è vuota
    if collection.count() == 0:
        print("DEBUG: Indicizzazione dati iniziale...")
        for fisioterapista in fisioterapisti:
            testo = f"{fisioterapista['nome']} - {fisioterapista['specializzazione']} - {fisioterapista['zona']}"
            collection.add(
                documents=[testo],
                metadatas=[fisioterapista],
                ids=[fisioterapista['nome']]
            )

        for i, linea in enumerate(linee_guida):
            collection.add(documents=[linea], ids=[f"linea-{i}"])
    
    _collection_cache = collection
    return collection

# Pipeline con Gemini
def rag_pipeline_demo(query):
    """Pipeline demo per il triage fisioterapico."""
    collection = setup_chroma()
    
    # Query ChromaDB
    risultati = collection.query(query_texts=[query], n_results=2)
    
    # ChromaDB 0.3.x restituisce una lista di liste per 'documents'
    if risultati['documents'] and len(risultati['documents']) > 0:
        risultati_testo = "\n".join(risultati['documents'][0])
    else:
        risultati_testo = "Nessuna informazione specifica trovata."

    prompt = f"""
    Domanda: {query}
    Informazioni Recuperate: {risultati_testo}

    In base ai risultati ottenuti, genera una risposta dettagliata ma concisa per il paziente.
    Rispondi in modo professionale come un assistente di triage fisioterapico.
    """

    return run_local_model(prompt)

# Esecuzione della Demo
if __name__ == "__main__":
    query = "Cerco un fisioterapista a domicilio per riabilitazione neurologica a Padova."
    risposta = rag_pipeline_demo(query)
    print("Risposta AI:", risposta)
