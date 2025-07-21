import json  # Still useful if you want to inspect output, but not for initial DB load
import chromadb
import os
import torch
from sentence_transformers import SentenceTransformer
import requests  # For interacting with Ollama API

# --- Configuration ---
# Removed EMBEDDINGS_FILE as we now directly use ChromaDB
CHROMA_DB_PATH = "./finacle_chroma_db"  # Directory where ChromaDB stores data (must match processing script)
QUERY_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"  # Model for embedding user queries
QUERY_TASK_TYPE = "search_query"  # Task type for embedding the query

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API endpoint
OLLAMA_MODEL_NAME = "my-finacle-model:latest"  # The Ollama model you want to use (must be pulled in Ollama)


# --- Helper Functions (reused and slightly modified) ---
def get_embedding_model(model_name=QUERY_MODEL_NAME):
    """
    Loads the Nomic Embed model for generating query embeddings.
    """
    print(f"Loading query embedding model: {model_name}...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    cache_dir = os.path.join(
        os.path.expanduser("~"), ".cache", "huggingface", "transformers"
    )
    os.makedirs(cache_dir, exist_ok=True)

    try:
        model = SentenceTransformer(
            model_name, trust_remote_code=True, device=device, cache_folder=cache_dir
        )
        return model
    except Exception as e:
        print(f"Error loading query embedding model '{model_name}': {e}")
        print(
            "Please ensure 'sentence-transformers' and 'torch' are correctly installed."
        )
        return None


def embed_query(query_text, model, task_type=QUERY_TASK_TYPE):
    """
    Generates an embedding for a given query text.
    """
    if model is None:
        return None

    prefixed_query = f"{task_type}: {query_text}"
    embedding = model.encode([prefixed_query], normalize_embeddings=True)
    return embedding[0].tolist()  # Return as a list of floats


def generate_ollama_response(
    prompt, model_name=OLLAMA_MODEL_NAME, api_url=OLLAMA_API_URL
):
    """
    Sends a prompt to the Ollama API and returns the generated response.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,  # Set to True if you want streaming response
    }

    try:
        print(f"Sending prompt to Ollama model '{model_name}'...")
        response = requests.post(
            api_url, headers=headers, json=data, timeout=300
        )  # Added timeout
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.json()
        return result.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Ollama server at {api_url}.")
        print(
            "Please ensure Ollama is running (`ollama serve`) and the API URL is correct."
        )
        return "Error: Ollama server not reachable."
    except requests.exceptions.Timeout:
        print(f"Error: Ollama request timed out after 300 seconds.")
        print(
            "The model might be taking too long to respond, or the prompt is too large."
        )
        return "Error: Ollama request timed out."
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama API: {e}")
        return f"Error: {e}"


# --- Main RAG Script ---
if __name__ == "__main__":
    # Ensure ChromaDB path exists
    if not os.path.exists(CHROMA_DB_PATH):
        print(f"Error: ChromaDB directory '{CHROMA_DB_PATH}' not found.")
        print(
            "Please run the 'process_all_pdfs_to_embeddings.py' script first to populate ChromaDB."
        )
        exit()

    # 1. Initialize ChromaDB client and connect to the existing collection
    print(f"Connecting to ChromaDB at {CHROMA_DB_PATH}...")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection_name = "finacle_documentation_chunks"  # This MUST match the name used in PDF processing script

    try:
        collection = client.get_collection(name=collection_name)
        if collection.count() == 0:
            print(f"Error: ChromaDB collection '{collection_name}' is empty.")
            print(
                "Please ensure 'process_all_pdfs_to_embeddings.py' ran successfully and populated the database."
            )
            exit()
        print(
            f"Successfully connected to ChromaDB collection '{collection_name}' with {collection.count()} items."
        )
    except Exception as e:
        print(f"Error connecting to ChromaDB collection '{collection_name}': {e}")
        print(
            "Please ensure 'process_all_pdfs_to_embeddings.py' ran successfully and created/populated the collection."
        )
        exit()

    # 2. Load the embedding model for queries
    query_embedding_model = get_embedding_model()
    if query_embedding_model is None:
        print("Failed to load query embedding model. Cannot perform RAG.")
        exit()

    # 3. RAG Query Loop
    print("\n--- Finacle RAG Chat with Mistral ---")
    print("Ask a question about Finacle scripting syntax (type 'exit' to quit).")

    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == "exit":
            break

        # Embed the user's query
        print("Embedding your query...")
        query_embedding = embed_query(user_query, query_embedding_model)
        if query_embedding is None:
            print("Could not embed query. Please try again.")
            continue

        # Perform semantic search in ChromaDB
        print("Searching for relevant Finacle documentation chunks...")
        search_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,  # Retrieve top 5 most relevant chunks
            include=["documents"],  # We only need the text content
        )

        retrieved_docs = (
            search_results["documents"][0]
            if search_results and search_results["documents"]
            else []
        )

        if not retrieved_docs:
            print(
                "No relevant documentation found for your query in the vector database."
            )
            # Optionally, still send to Ollama with just the query
            # or tell the user to rephrase.
            final_prompt = f"Question: {user_query}\n\nAnswer the question concisely."
            print("No context found from documentation, asking Mistral directly...")
        else:
            # Build the context for the LLM
            context_string = "\n\n".join(retrieved_docs)

            # Construct the prompt for Mistral
            # This prompt engineering is crucial for good RAG performance
            final_prompt = f"""
You are an expert on Finacle scripting syntax. Use the provided Finacle documentation below to answer the user's question.
If the answer cannot be found in the provided documentation, state that clearly and do not make up information.

Finacle Documentation Context:
{context_string}

User Question: {user_query}

Finacle Expert Answer:
"""
            print(f"Retrieved {len(retrieved_docs)} chunks. Asking Mistral...")

        # Get response from Ollama
        ollama_response = generate_ollama_response(final_prompt, OLLAMA_MODEL_NAME)

        print("\n--- Mistral's Answer ---")
        print(ollama_response)
        print("------------------------")

    print("Exiting RAG chat. Goodbye!")
