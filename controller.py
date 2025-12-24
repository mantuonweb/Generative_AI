import uuid
from typing import List, Dict, Any
from rag_engine import RAGEngine
from utils import process_pdf_file

class RAGController:
    """Controller for RAG operations"""
    
    def __init__(self, llm_model: str = "llama2"):
        self.rag = RAGEngine(llm_model=llm_model)
        self.rag.load_state()
    
    def upload_pdf(self, pdf_content: bytes, filename: str) -> Dict[str, Any]:
        """Process and store PDF content"""
        # Validate file extension
        if not filename.endswith('.pdf'):
            raise ValueError("Only PDF files are allowed")
        
        # Process PDF and get chunks
        chunks = process_pdf_file(pdf_content)
        
        # Add each chunk to RAG engine
        for chunk in chunks:
            doc_id = str(uuid.uuid4())
            self.rag.add_document(doc_id, chunk, filename)
        
        # Save state
        self.rag.save_state()
        
        return {
            "message": "PDF processed successfully",
            "filename": filename,
            "chunks_created": len(chunks),
            "total_chunks": len(self.rag.chunks)
        }
    
    def query_documents(self, query: str, top_k: int = 3, template_type: str = "default") -> Dict[str, Any]:
        """Query the RAG system"""
        if len(self.rag.chunks) == 0:
            raise ValueError("No documents uploaded yet")
        
        result = self.rag.generate_answer(query, top_k, template_type)
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""
        return {
            "total_chunks": len(self.rag.chunks),
            "total_documents": len(set([m['filename'] for m in self.rag.metadata])),
            "index_size": self.rag.index.ntotal
        }
    
    def clear_all(self) -> Dict[str, str]:
        """Clear all data from the system"""
        self.rag.clear()
        return {"message": "All data cleared"}
    
    def has_documents(self) -> bool:
        """Check if any documents are loaded"""
        return len(self.rag.chunks) > 0