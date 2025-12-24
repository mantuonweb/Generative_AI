import uuid
from typing import List, Dict, Any, Optional
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
    
    def query_documents(self, query: str, top_k: int = 3, template_type: str = "default", 
                       filter_filenames: Optional[List[str]] = None) -> Dict[str, Any]:
        """Query the RAG system with optional document filtering"""
        if len(self.rag.chunks) == 0:
            raise ValueError("No documents uploaded yet")
        
        # Validate filter_filenames if provided
        if filter_filenames:
            available_docs = self.get_document_list()
            invalid_docs = [f for f in filter_filenames if f not in available_docs]
            if invalid_docs:
                raise ValueError(f"Documents not found: {', '.join(invalid_docs)}")
        
        result = self.rag.generate_answer(query, top_k, template_type, filter_filenames)
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""
        return {
            "total_chunks": len(self.rag.chunks),
            "total_documents": len(set([m['filename'] for m in self.rag.metadata])),
            "index_size": self.rag.index.ntotal
        }
    
    def get_document_list(self) -> List[str]:
        """Get list of all uploaded documents"""
        if not self.rag.metadata:
            return []
        return list(set([m['filename'] for m in self.rag.metadata]))
    
    def get_document_details(self) -> List[Dict[str, Any]]:
        """Get detailed information about each document"""
        if not self.rag.metadata:
            return []
        
        doc_info = {}
        for meta in self.rag.metadata:
            filename = meta['filename']
            if filename not in doc_info:
                doc_info[filename] = {
                    'filename': filename,
                    'chunk_count': 0
                }
            doc_info[filename]['chunk_count'] += 1
        
        return list(doc_info.values())
    
    def get_document_chunks(self, filename: str) -> Dict[str, Any]:
        """Get all chunks from a specific document"""
        chunks = [
            {
                'id': meta['id'],
                'content': content,
                'preview': content[:200] + '...' if len(content) > 200 else content
            }
            for meta, content in zip(self.rag.metadata, self.rag.chunks)
            if meta['filename'] == filename
        ]
        
        if not chunks:
            raise ValueError(f"Document not found: {filename}")
        
        return {
            'filename': filename,
            'chunk_count': len(chunks),
            'chunks': chunks
        }
    
    def delete_document(self, filename: str) -> Dict[str, Any]:
        """Delete a specific document and its chunks"""
        if filename not in self.get_document_list():
            raise ValueError(f"Document not found: {filename}")
        
        # Count chunks before deletion
        chunks_before = len(self.rag.chunks)
        
        # Filter out chunks from the specified document
        new_chunks = []
        new_metadata = []
        for meta, chunk in zip(self.rag.metadata, self.rag.chunks):
            if meta['filename'] != filename:
                new_chunks.append(chunk)
                new_metadata.append(meta)
        
        # Rebuild FAISS index
        self.rag.chunks = new_chunks
        self.rag.metadata = new_metadata
        self.rag.index = faiss.IndexFlatL2(self.rag.dimension)
        
        # Re-add all remaining chunks to index
        if new_chunks:
            embeddings = self.rag.embedding_model.encode(new_chunks)
            self.rag.index.add(np.array(embeddings, dtype=np.float32))
        
        # Save state
        self.rag.save_state()
        
        chunks_deleted = chunks_before - len(new_chunks)
        
        return {
            "message": f"Document '{filename}' deleted successfully",
            "chunks_deleted": chunks_deleted,
            "remaining_chunks": len(new_chunks)
        }
    
    def clear_all(self) -> Dict[str, str]:
        """Clear all data from the system"""
        self.rag.clear()
        return {"message": "All data cleared"}
    
    def has_documents(self) -> bool:
        """Check if any documents are loaded"""
        return len(self.rag.chunks) > 0