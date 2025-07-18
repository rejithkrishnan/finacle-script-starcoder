import os
import re
import json
from google.cloud import storage
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
import PyPDF2
from io import BytesIO

# --- Configuration ---
PROJECT_ID = "potatoflix-3ce96"  # <--- REPLACE with your project ID
LOCATION = "us-central1"  # <--- REPLACE with your region (e.g., "us-central1")
GCS_BUCKET_NAME = "finacle-copilot"  # <--- REPLACE with your bucket name
PDF_FILE_NAME = "Scripting Syntax.pdf"
LOCAL_EMBEDDINGS_FILE = "embeddings.json"
LOCAL_DOCUMENTS_FILE = "documents.json"
# --------------------


def download_pdf_from_gcs(bucket_name, source_blob_name):
    """Downloads a PDF from GCS into memory."""
    print(f"Downloading {source_blob_name} from bucket {bucket_name}...")
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    pdf_as_bytes = blob.download_as_bytes()
    return BytesIO(pdf_as_bytes)


def parse_pdf_to_chunks(pdf_file_object):
    """Parses a PDF file object and splits the text into chunks (paragraphs)."""
    print("Parsing PDF and chunking text...")
    pdf_reader = PyPDF2.PdfReader(pdf_file_object)
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text() + "\n"

    # Split text into chunks based on paragraphs (two or more newlines)
    chunks = re.split(r"\n\s*\n", full_text)
    # Filter out very small or empty chunks
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]
    print(f"Created {len(chunks)} text chunks from the PDF.")
    return chunks


def generate_embeddings(text_chunks):
    """Generates embeddings for a list of text chunks using Vertex AI."""
    print("Initializing Vertex AI and loading embedding model...")
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    print(f"Generating embeddings for {len(text_chunks)} chunks...")
    embeddings = []
    # The API can handle batches of up to 250, but we'll do 5 for demonstration
    batch_size = 5
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i : i + batch_size]
        # The get_embeddings API call
        vectors = model.get_embeddings(batch)
        for i, vector in enumerate(vectors):
            embeddings.append(
                {
                    "id": str(len(embeddings) + 1),  # Simple numeric ID
                    "embedding": vector.values,
                }
            )
        print(f"  ...processed batch {i//batch_size + 1}")

    return embeddings


def main():
    pdf_file = download_pdf_from_gcs(GCS_BUCKET_NAME, PDF_FILE_NAME)
    text_chunks = parse_pdf_to_chunks(pdf_file)
    embeddings = generate_embeddings(text_chunks)

    # --- CORRECTED SAVING LOGIC ---
    # Save the generated embeddings in JSON Lines format.
    print(f"Saving embeddings to {LOCAL_EMBEDDINGS_FILE} in JSON Lines format...")
    with open(LOCAL_EMBEDDINGS_FILE, "w") as f:
        for item in embeddings:
            f.write(json.dumps(item) + "\n")  # Write each JSON object on a new line

    # Save the original text chunks with their IDs for later retrieval
    documents_with_ids = {str(i + 1): chunk for i, chunk in enumerate(text_chunks)}
    with open(LOCAL_DOCUMENTS_FILE, "w") as f:
        json.dump(documents_with_ids, f, indent=2)
    print(f"Original document chunks saved to {LOCAL_DOCUMENTS_FILE}")


if __name__ == "__main__":
    main()
