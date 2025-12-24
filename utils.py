import io
from PyPDF2 import PdfReader
from typing import List

class TemplateManager:
    """Simple template manager for RAG prompts"""
    
    # Prompt Templates
    DEFAULT = """Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
    
    DETAILED = """You are a helpful assistant. Use the following context to answer the question in detail.

Context:
{context}

Question: {query}

Provide a comprehensive answer:"""
    
    CONCISE = """Answer briefly using only the context provided.

Context:
{context}

Question: {query}

Brief Answer:"""
    
    @staticmethod
    def get(template_type: str = "default") -> str:
        """Get template by type"""
        templates = {
            "default": TemplateManager.DEFAULT,
            "detailed": TemplateManager.DETAILED,
            "concise": TemplateManager.CONCISE
        }
        return templates.get(template_type, TemplateManager.DEFAULT)


def process_pdf_file(pdf_content: bytes, chunk_size: int = 500) -> List[str]:
    """Process PDF file and extract text chunks"""
    pdf_file = io.BytesIO(pdf_content)
    pdf_reader = PdfReader(pdf_file)
    
    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Split into chunks
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks
