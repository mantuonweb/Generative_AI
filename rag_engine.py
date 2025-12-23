import numpy as np
from sentence_transformers import SentenceTransformer
import ollama
from typing import List, Dict
import os
import faiss
import pickle

class RAGEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2", llm_model="llama3.2"):
        print(f"🔄 Initializing RAG Engine with FAISS...")
        self.embedding_model = SentenceTransformer(model_name)
        self.llm_model = llm_model
        self.dimension = 384  # all-MiniLM-L6-v2 embedding size
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
        self.metadata = []
        print(f"✅ RAG Engine initialized with FAISS")
    
    def add_document(self, doc_id: str, content: str, filename: str):
        """Add a document chunk to FAISS vector store"""
        # Generate embedding
        embedding = self.embedding_model.encode([content])[0]
        
        # Add to FAISS index
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Store chunk and metadata
        self.chunks.append(content)
        self.metadata.append({
            'id': doc_id,
            'filename': filename
        })
        
        print(f"✅ Added chunk from: {filename} (Total chunks: {len(self.chunks)})")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks based on query"""
        if not self.chunks:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        query_vector = np.array(query_embedding, dtype=np.float32)
        
        # Search in FAISS
        distances, indices = self.index.search(query_vector, min(top_k, len(self.chunks)))
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                # Convert L2 distance to similarity score (0-1)
                similarity = 1 / (1 + distances[0][i])
                results.append({
                    'id': self.metadata[idx]['id'],
                    'filename': self.metadata[idx]['filename'],
                    'content': self.chunks[idx],
                    'score': float(similarity)
                })
        
        return results
    
    def generate_answer(self, query: str, top_k: int = 3) -> Dict:
        """Generate answer using RAG"""
        # Search for relevant chunks
        results = self.search(query, top_k)
        
        if not results:
            return {
                'answer': 'No relevant information found in the documents.',
                'sources': []
            }
        
        # Build context from results
        context = "\n\n".join([r['content'] for r in results])
        
        # Create prompt
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate answer using Ollama
        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt
            )
            answer = response['response']
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"
        
        return {
            'answer': answer,
            'sources': [r['content'][:200] + '...' for r in results],
            'num_sources': len(results)
        }
    
    def get_all_documents(self) -> List[Dict]:
        """Get all stored chunks"""
        return [
            {
                'id': meta['id'],
                'filename': meta['filename'],
                'content': content
            }
            for meta, content in zip(self.metadata, self.chunks)
        ]
    
    def save_state(self, filepath: str = "data/rag_state.pkl"):
        """Save FAISS index and data to disk"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, filepath.replace('.pkl', '.faiss'))
        
        # Save metadata and chunks
        state = {
            'chunks': self.chunks,
            'metadata': self.metadata
        }
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
        
        print(f"💾 Saved state to {filepath}")
    
    def load_state(self, filepath: str = "data/rag_state.pkl"):
        """Load FAISS index and data from disk"""
        faiss_path = filepath.replace('.pkl', '.faiss')
        
        if os.path.exists(filepath) and os.path.exists(faiss_path):
            # Load FAISS index
            self.index = faiss.read_index(faiss_path)
            
            # Load metadata and chunks
            with open(filepath, 'rb') as f:
                state = pickle.load(f)
                self.chunks = state['chunks']
                self.metadata = state['metadata']
            
            print(f"📂 Loaded {len(self.chunks)} chunks from {filepath}")
            return True
        return False
    
    def clear(self):
        """Clear all data"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
        self.metadata = []
        print("🗑️ Cleared all data")