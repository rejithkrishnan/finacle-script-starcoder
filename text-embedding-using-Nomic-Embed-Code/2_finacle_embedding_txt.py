import os
import torch
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm  # For a nice progress bar


def read_text_file(file_path):
    """
    Reads content from a plain text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f"Error: Text file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading text file '{file_path}': {e}")
        return None


def chunk_text(text, chunk_size=1000, overlap=100):
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
        # Ensure start doesn't go negative on the last chunk if overlap is large
        if start < 0:
            start = 0
    return chunks


def generate_nomic_embeddings_local(
    text_chunks,
    model_name="nomic-ai/nomic-embed-text-v1.5",
    task_type="search_document",
):
    """
    Generates text embeddings using Nomic Embed Code (nomic-ai/nomic-embed-text-v1.5) locally.

    Args:
        text_chunks (list[str]): A list of text chunks to embed.
        model_name (str): The Hugging Face model identifier for Nomic Embed Code.
        task_type (str): The task type for instruction tuning (e.g., "search_document").
                         Nomic Embed models are instruction-tuned, so this prefix is crucial.

    Returns:
        list[list[float]]: A list of embeddings.
    """
    print(f"Loading local model: {model_name}...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Ensure cache directory exists for Hugging Face models
    cache_dir = os.path.join(
        os.path.expanduser("~"), ".cache", "huggingface", "transformers"
    )
    os.makedirs(cache_dir, exist_ok=True)

    try:
        model = SentenceTransformer(
            model_name, trust_remote_code=True, device=device, cache_folder=cache_dir
        )
    except Exception as e:
        print(f"Error loading model '{model_name}': {e}")
        print(
            "Please ensure 'sentence-transformers' and 'torch' are correctly installed."
        )
        print("If using GPU, ensure CUDA is properly set up.")
        return []

    # Add task instruction prefixes as required by nomic-embed-text-v1.5
    prefixed_texts = [f"{task_type}: {chunk}" for chunk in text_chunks]

    print("Generating embeddings locally...")
    # encode method can take a list of strings
    embeddings = model.encode(
        prefixed_texts, show_progress_bar=True, normalize_embeddings=True
    )
    return embeddings.tolist()  # Convert numpy array to list for JSON serialization


def process_text_file_for_embeddings(text_file_path, chunk_size=1000, overlap=100):
    """
    Reads a text file, chunks its content, and generates Nomic embeddings locally.
    """
    print(f"Reading text from {text_file_path}...")
    full_text = read_text_file(text_file_path)

    if full_text is None:
        return [], []  # Return empty lists if text reading fails

    print("Text read successfully. Chunking text...")
    chunks = chunk_text(full_text, chunk_size, overlap)

    print(f"Generated {len(chunks)} chunks.")
    if not chunks:
        print("No chunks generated. The file might be empty or too small.")
        return [], []

    embeddings = generate_nomic_embeddings_local(chunks)

    print(f"Generated {len(embeddings)} embeddings.")
    return embeddings, chunks


if __name__ == "__main__":
    # --- Configuration ---
    text_file = "Scripting Syntax.txt"  # Name of your plain text file
    output_json_file = "finacle_embeddings_from_txt.json"
    chunk_size = 1000  # Number of characters per chunk
    overlap = 100  # Number of overlapping characters between chunks

    # --- Main execution ---
    if not os.path.exists(text_file):
        print(f"Error: Text file '{text_file}' not found.")
        print(
            "Please make sure the text file is in the same directory as the script, or provide the full path."
        )
    else:
        embeddings, chunks = process_text_file_for_embeddings(
            text_file, chunk_size, overlap
        )

        if embeddings:
            print("\nFirst 5 embeddings (first 10 dimensions):")
            for i, emb in enumerate(embeddings[:5]):
                print(f"Chunk {i+1}: {emb[:10]}...")

            print(f"\nTotal embeddings generated: {len(embeddings)}")
            if (
                embeddings and embeddings[0]
            ):  # Check if embeddings list is not empty and its first element is not empty
                print(f"Dimension of each embedding: {len(embeddings[0])}")

            # Save embeddings and chunks to a JSON file
            output_data = []
            for i in range(len(embeddings)):
                output_data.append({"chunk": chunks[i], "embedding": embeddings[i]})

            with open(output_json_file, "w") as f:
                json.dump(output_data, f, indent=4)
            print(f"\nEmbeddings and chunks saved to {output_json_file}")
        else:
            print("\nNo embeddings were generated. Please check for errors above.")
