from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
import io
import uuid
from rag_engine import RAGEngine

app = FastAPI()

# Initialize RAG Engine
rag = RAGEngine(llm_model="llama2")

# Try to load existing state
rag.load_state()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def create_chunks(text):
    """Split text into chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF and store in vector database"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        # Read PDF
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        
        # Create chunks
        chunks = create_chunks(text)
        
        # Add each chunk to RAG engine
        for chunk in chunks:
            doc_id = str(uuid.uuid4())
            rag.add_document(doc_id, chunk, file.filename)
        
        # Save state
        rag.save_state()
        
        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "total_chunks": len(rag.chunks)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(data: dict):
    """Query the RAG system"""
    query_text = data.get("query", "")
    top_k = data.get("top_k", 3)
    
    if not query_text:
        raise HTTPException(status_code=400, detail="Query is required")
    
    if len(rag.chunks) == 0:
        raise HTTPException(status_code=404, detail="No documents uploaded yet")
    
    try:
        result = rag.generate_answer(query_text, top_k)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {
        "message": "Simple RAG Application",
        "endpoints": {
            "upload": "POST /upload-pdf",
            "query": "POST /query",
            "stats": "GET /stats",
            "clear": "DELETE /clear"
        }
    }

@app.get("/stats")
def stats():
    return {
        "total_chunks": len(rag.chunks),
        "total_documents": len(set([m['filename'] for m in rag.metadata])),
        "index_size": rag.index.ntotal
    }

@app.delete("/clear")
def clear():
    """Clear all data"""
    rag.clear()
    return {"message": "All data cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)