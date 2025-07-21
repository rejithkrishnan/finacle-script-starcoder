import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import os
import torch
import json
from tqdm import tqdm  # For a nice progress bar
import chromadb

# --- Configuration ---
PDF_DIRECTORY = "./finacle_pdfs"  # Directory containing your Finacle PDF files
CHROMA_DB_PATH = "./finacle_chroma_db"  # Directory where ChromaDB will store data
MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
TASK_TYPE = "search_document"  # Task type for embedding document content
CHUNK_SIZE = 1000  # Number of characters per chunk
OVERLAP = 100  # Number of overlapping characters between chunks


# --- Helper Functions (reused and slightly modified) ---
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    Returns (text, True) on success, (None, False) on failure.
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text, True
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return None, False


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Splits a long text into smaller chunks with optional overlap.
    """
    chunks = []
    if not text:
        return chunks

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        if start < 0:
            start = 0
    return chunks


def get_embedding_model(model_name=MODEL_NAME):
    """
    Loads the Nomic Embed model.
    """
    print(f"Loading embedding model: {model_name}...")
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
        print(f"Error loading model '{model_name}': {e}")
        print(
            "Please ensure 'sentence-transformers' and 'torch' are correctly installed."
        )
        return None


# --- Main Script ---
if __name__ == "__main__":
    # Ensure the PDF directory exists
    if not os.path.exists(PDF_DIRECTORY):
        print(f"Error: PDF directory '{PDF_DIRECTORY}' not found.")
        print(
            "Please create this directory and place your Finacle PDF files inside it."
        )
        exit()

    # Initialize ChromaDB client and collection
    print(f"Initializing ChromaDB at {CHROMA_DB_PATH}...")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection_name = "finacle_documentation_chunks"

    # Create or get the collection. We'll clear it for a fresh start each run if needed.
    # For production, you might want to update existing documents instead of clearing.
    try:
        collection = client.get_collection(name=collection_name)
        print(
            f"ChromaDB collection '{collection_name}' already exists. Clearing for fresh import..."
        )
        client.delete_collection(name=collection_name)
        collection = client.create_collection(name=collection_name)
    except Exception:  # Collection does not exist
        print(
            f"ChromaDB collection '{collection_name}' not found. Creating new collection..."
        )
        collection = client.create_collection(name=collection_name)

    # Load the embedding model once
    embedding_model = get_embedding_model()
    if embedding_model is None:
        print("Failed to load embedding model. Exiting.")
        exit()

    all_documents_for_db = []
    all_embeddings_for_db = []
    all_ids_for_db = []

    # Iterate through all PDF files in the directory
    pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in '{PDF_DIRECTORY}'. Exiting.")
        exit()

    print(f"\nFound {len(pdf_files)} PDF files in '{PDF_DIRECTORY}'.")

    current_id_counter = 0
    for pdf_file_name in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_file_name)
        print(f"\nProcessing: {pdf_path}")

        # 1. Extract text
        full_text, success = extract_text_from_pdf(pdf_path)
        if not success or not full_text:
            continue  # Skip to next PDF if extraction failed or text is empty

        # 2. Chunk text
        chunks = chunk_text(full_text, CHUNK_SIZE, OVERLAP)
        if not chunks:
            print(f"No chunks generated for '{pdf_file_name}'. Skipping.")
            continue

        print(f"Generated {len(chunks)} chunks for '{pdf_file_name}'.")

        # 3. Generate embeddings for these chunks
        # Add task instruction prefixes for document embedding
        prefixed_chunks = [f"{TASK_TYPE}: {chunk}" for chunk in chunks]

        # Using a separate tqdm for batch encoding progress
        print("Generating embeddings for chunks...")
        embeddings = embedding_model.encode(
            prefixed_chunks, show_progress_bar=True, normalize_embeddings=True
        )
        embeddings_list = embeddings.tolist()

        # Prepare data for adding to ChromaDB
        for i, chunk_content in enumerate(chunks):
            unique_id = (
                f"{pdf_file_name.replace('.pdf', '')}_chunk_{current_id_counter}"
            )
            all_documents_for_db.append(chunk_content)
            all_embeddings_for_db.append(embeddings_list[i])
            all_ids_for_db.append(unique_id)
            current_id_counter += 1

    if not all_documents_for_db:
        print("No documents were processed and embedded. Exiting.")
        exit()

    # 4. Add all processed data to ChromaDB
    print(
        f"\nAdding all {len(all_documents_for_db)} chunks to ChromaDB collection '{collection_name}'..."
    )
    # Add in batches if your dataset is very large.
    # ChromaDB's add method can handle large lists, but very large might benefit from manual batching.
    collection.add(
        embeddings=all_embeddings_for_db,
        documents=all_documents_for_db,
        ids=all_ids_for_db,
    )
    print(f"Successfully added {collection.count()} items to ChromaDB.")
    print(f"Total embeddings generated from all PDFs: {len(all_embeddings_for_db)}")
    print(
        f"Dimension of each embedding: {len(all_embeddings_for_db[0]) if all_embeddings_for_db else 'N/A'}"
    )

    # Optional: Save a manifest of all documents and their IDs added
    manifest_data = [
        {"id": _id, "chunk_content": doc}
        for _id, doc in zip(all_ids_for_db, all_documents_for_db)
    ]
    with open("finacle_processed_docs_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=4)
    print(
        "\nManifest of processed documents saved to finacle_processed_docs_manifest.json"
    )

    print(
        "\nProcessing complete. You can now use the 'finacle_rag_ollama.py' script for RAG."
    )
