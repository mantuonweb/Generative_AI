from PyPDF2 import PdfReader
import io

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def create_chunks(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split text into chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks

def process_pdf_file(pdf_content):
    """Process PDF content and return chunks"""
    pdf_file = io.BytesIO(pdf_content)
    text = extract_text_from_pdf(pdf_file)
    chunks = create_chunks(text)
    return chunks
