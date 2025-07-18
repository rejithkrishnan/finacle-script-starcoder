import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import os
import torch


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text


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
    # Use 'cuda' if a GPU is available, otherwise 'cpu'
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

    # Add task instruction prefixes as required by nomic-embed-text-v1.5
    prefixed_texts = [f"{task_type}: {chunk}" for chunk in text_chunks]

    print("Generating embeddings locally...")
    # encode method can take a list of strings
    embeddings = model.encode(
        prefixed_texts, show_progress_bar=True, normalize_embeddings=True
    )
    return embeddings.tolist()  # Convert numpy array to list for JSON serialization


def process_pdf_for_embeddings_local(pdf_path, chunk_size=1000, overlap=100):
    """
    Extracts text from a PDF, chunks it, and generates Nomic embeddings locally.
    """
    print(f"Extracting text from {pdf_path}...")
    full_text = extract_text_from_pdf(pdf_path)

    if full_text is None:
        return []

    print("Text extracted. Chunking text...")
    # Simple chunking logic (can be improved)
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        if start < 0:
            start = 0

    print(f"Generated {len(chunks)} chunks.")
    embeddings = generate_nomic_embeddings_local(chunks)

    print(f"Generated {len(embeddings)} embeddings.")
    return embeddings, chunks


if __name__ == "__main__":
    pdf_file = "finacle_scripting_syntax.pdf"  # Replace with your PDF file name

    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found.")
        print(
            "Please make sure the PDF is in the same directory as the script, or provide the full path."
        )
    else:
        embeddings, chunks = process_pdf_for_embeddings_local(pdf_file)

        if embeddings:
            print("\nFirst 5 embeddings (first 10 dimensions):")
            for i, emb in enumerate(embeddings[:5]):
                print(f"Chunk {i+1}: {emb[:10]}...")

            print(f"\nTotal embeddings generated: {len(embeddings)}")
            print(f"Dimension of each embedding: {len(embeddings[0])}")

            # Save embeddings and chunks
            import json

            output_data = []
            for i in range(len(embeddings)):
                output_data.append({"chunk": chunks[i], "embedding": embeddings[i]})

            with open("finacle_embeddings_local.json", "w") as f:
                json.dump(output_data, f, indent=4)
            print("\nEmbeddings and chunks saved to finacle_embeddings_local.json")
