from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from controller import RAGController

app = FastAPI()

# Initialize Controller
controller = RAGController(llm_model="llama2")

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The query text")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top results to retrieve")
    template_type: str = Field(default="default", description="Template type: default, detailed, concise")

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF and store in vector database"""
    try:
        # Read PDF content
        pdf_content = await file.read()
        
        # Delegate to controller
        result = controller.upload_pdf(pdf_content, file.filename)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(request: QueryRequest):
    """Query the RAG system"""
    try:
        # Delegate to controller
        result = controller.query_documents(request.query, request.top_k, request.template_type)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    """API information"""
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
    """Get system statistics"""
    try:
        return controller.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
def clear():
    """Clear all data"""
    try:
        return controller.clear_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
