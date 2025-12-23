# Simple RAG Application 🚀

A simple Retrieval Augmented Generation (RAG) application that allows you to upload PDF documents, store them in a FAISS vector database, and query them using Ollama LLM for intelligent question-answering.

## 🎯 Features

- ✅ **PDF Upload & Processing** - Automatically extract and chunk text from PDFs
- ✅ **FAISS Vector Store** - Efficient similarity search with Facebook's FAISS
- ✅ **Semantic Search** - Find relevant content using sentence transformers
- ✅ **AI-Powered Answers** - Generate contextual answers using Ollama (Llama2/Llama3.2)
- ✅ **Persistent Storage** - Data saved to disk and auto-loads on restart
- ✅ **REST API** - Simple FastAPI endpoints
- ✅ **No Docker Required** - Run directly on your machine
- ✅ **Interactive Testing** - Multiple ways to query your documents

## 📋 Prerequisites

- **Python 3.8+** (Python 3.11+ recommended)
- **Ollama** installed on your system
- **8GB+ RAM** recommended
- **macOS, Linux, or Windows**

## 🚀 Quick Start

### 1. Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [https://ollama.com/download](https://ollama.com/download)

### 2. Pull AI Models

```bash
ollama pull llama2
```

Or for faster responses:
```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Start Ollama Server

**Terminal 1:**
```bash
ollama serve
```

Keep this running in the background.

### 5. Start RAG Application

**Terminal 2:**
```bash
python3 app.py
```

The application will start on `http://localhost:8000`

### 6. Upload a PDF and Query

**Terminal 3:**
```bash
# Create a sample PDF (optional)
python3 create_sample_pdf.py

# Upload your PDF
python3 test.py upload sample.pdf

# Ask questions
python3 test.py query "What is this document about?"
```

## 📁 Project Structure

```
simple-rag/
├── rag_engine.py           # Core RAG engine with FAISS
├── app.py                  # FastAPI application
├── test.py                 # CLI test script
├── interactive_query.py    # Interactive query mode
├── create_sample_pdf.py    # Sample PDF generator
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Persistent storage (auto-created)
│   ├── rag_state.pkl     # Chunks and metadata
│   └── rag_state.faiss   # FAISS vector index
└── *.pdf                  # Your uploaded PDFs
```

## 🎮 Usage Guide

### Method 1: Command Line Interface

**Upload a PDF:**
```bash
python3 test.py upload document.pdf
```

**Ask Questions:**
```bash
python3 test.py query "What is the main topic?"
python3 test.py query "Explain the key concepts"
python3 test.py query "Summarize the document"
```

**Check Statistics:**
```bash
python3 test.py stats
```

**Clear All Data:**
```bash
python3 test.py clear
```

### Method 2: Interactive Mode

```bash
python3 interactive_query.py
```

Then type your questions interactively:
```
❓ Your question: What is this document about?
❓ Your question: Explain the main points
❓ Your question: exit
```

### Method 3: Using cURL

**Upload PDF:**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload-pdf
```

**Query:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI?", "top_k": 3}'
```

**Get Stats:**
```bash
curl http://localhost:8000/stats
```

### Method 4: Interactive API Documentation

Open your browser:
```
http://localhost:8000/docs
```

Use the Swagger UI to test all endpoints interactively.

### Method 5: Python Code

```python
import requests

# Upload PDF
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload-pdf', files=files)
    print(response.json())

# Query
response = requests.post(
    'http://localhost:8000/query',
    json={'query': 'What is this about?', 'top_k': 3}
)
result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {result['num_sources']}")
```

## 🔌 API Endpoints

### `GET /`
Get API information and available endpoints

**Response:**
```json
{
  "message": "Simple RAG Application",
  "endpoints": {
    "upload": "POST /upload-pdf",
    "query": "POST /query",
    "stats": "GET /stats",
    "clear": "DELETE /clear"
  }
}
```

### `POST /upload-pdf`
Upload and process a PDF document

**Request:**
- Form data with `file` field (PDF only)

**Response:**
```json
{
  "message": "PDF processed successfully",
  "filename": "document.pdf",
  "chunks_created": 150,
  "total_chunks": 1930
}
```

### `POST /query`
Query the RAG system with a question

**Request:**
```json
{
  "query": "What is the role of the President?",
  "top_k": 3
}
```

**Response:**
```json
{
  "answer": "The President of India is the head of state...",
  "sources": [
    "Source chunk 1...",
    "Source chunk 2...",
    "Source chunk 3..."
  ],
  "num_sources": 3
}
```

**Parameters:**
- `query` (required): Your question
- `top_k` (optional, default=3): Number of relevant chunks to retrieve

### `GET /stats`
Get system statistics

**Response:**
```json
{
  "total_chunks": 1930,
  "total_documents": 1,
  "index_size": 1930
}
```

### `DELETE /clear`
Clear all stored data

**Response:**
```json
{
  "message": "All data cleared"
}
```

## ⚙️ Configuration

### Chunk Settings (in `app.py`)

```python
CHUNK_SIZE = 500        # Characters per chunk
CHUNK_OVERLAP = 50      # Overlap between chunks
```

### Model Settings (in `rag_engine.py`)

```python
class RAGEngine:
    def __init__(
        self, 
        model_name="all-MiniLM-L6-v2",  # Embedding model
        llm_model="llama2"               # LLM for generation
    ):
```

**Available LLM Models:**
- `llama2` - 3.8GB, good quality
- `llama3.2` - 2.0GB, faster, good quality
- `mistral` - 4.1GB, excellent quality
- `phi3` - 2.3GB, fast and efficient
- `gemma2` - 5.4GB, high quality

To change the model:
1. Pull the model: `ollama pull mistral`
2. Update `rag_engine.py`: `llm_model="mistral"`
3. Restart the app

## 📊 How It Works

```
┌─────────────┐
│  Upload PDF │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Extract Text   │
│  (PyPDF2)       │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Create Chunks  │
│  (500 chars)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Generate       │
│  Embeddings     │
│  (384-dim)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Store in FAISS │
│  Vector DB      │
└─────────────────┘

┌─────────────┐
│  User Query │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Convert to     │
│  Embedding      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Search FAISS   │
│  (top-k chunks) │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Build Context  │
│  from Chunks    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Send to Ollama │
│  with Prompt    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Return Answer  │
│  + Sources      │
└─────────────────┘
```

## 🎓 Example Workflow

### Example 1: Constitution of India

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start RAG app
python3 app.py

# Terminal 3: Upload and query
python3 test.py upload constitution.pdf
python3 test.py query "What is the role of the President?"
python3 test.py query "Explain the appointment of Ministers"
python3 test.py query "What are the powers of the Supreme Court?"
```

**Sample Output:**
```
🔍 QUESTION: What is the role of the President?
================================================================================

💡 ANSWER:
--------------------------------------------------------------------------------
The President of India is the head of state and is appointed by an electoral 
college. The President holds office during the pleasure of the electoral 
college and has various constitutional powers including...

📚 SOURCES USED: 3
--------------------------------------------------------------------------------

[Source 1]
ITUTION OF INDIA (Part V.—The Union)35 (5) A Minister who for any period...

[Source 2]
The President shall appoint as Prime Minister the leader of the political...

[Source 3]
63. The Vice-President of India. —There shall be a Vice-President of India...
```

### Example 2: Research Paper

```bash
python3 test.py upload research_paper.pdf
python3 test.py query "What is the main hypothesis?"
python3 test.py query "What methodology was used?"
python3 test.py query "What are the key findings?"
python3 test.py query "What are the limitations?"
```

### Example 3: Technical Documentation

```bash
python3 test.py upload api_documentation.pdf
python3 test.py query "How do I authenticate?"
python3 test.py query "What are the rate limits?"
python3 test.py query "Show me example API calls"
```

## 🔧 Troubleshooting

### Issue: "Cannot connect to Ollama"

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Verify it's accessible
curl http://localhost:11434/api/tags
```

### Issue: "404 error on /api/generate"

**Solution:**
```bash
# Check installed models
ollama list

# Pull the model
ollama pull llama2

# Test the model
ollama run llama2 "Hello"
```

### Issue: "FAISS installation failed"

**Solution:**
```bash
# Try without cache
pip3 install faiss-cpu --no-cache-dir

# Or use conda
conda install -c conda-forge faiss-cpu
```

### Issue: "Port 8000 already in use"

**Solution:**
```python
# Edit app.py, change port:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### Issue: "Slow response times"

**Solutions:**
1. Use a smaller model:
```bash
ollama pull llama3.2  # Faster than llama2
```

2. Reduce `top_k`:
```bash
python3 test.py query "question" --top_k 2
```

3. Use GPU acceleration (if available):
```bash
# Ollama automatically uses GPU on macOS (Metal)
# Check logs for: "inference compute" with Metal/CUDA
```

### Issue: "Out of memory"

**Solutions:**
1. Use a smaller model (llama3.2 or phi3)
2. Reduce chunk size in `app.py`
3. Clear old data: `python3 test.py clear`

### Issue: "PDF text extraction failed"

**Solution:**
```bash
# Install additional dependencies
pip3 install pdfplumber

# Or try OCR for scanned PDFs
pip3 install pytesseract
```

## 📦 Dependencies

```
fastapi          # Web framework
uvicorn          # ASGI server
PyPDF2           # PDF text extraction
sentence-transformers  # Text embeddings
faiss-cpu        # Vector similarity search
numpy            # Numerical operations
ollama           # LLM integration
python-multipart # File upload support
reportlab        # PDF generation (for samples)
```

## 🚀 Performance Tips

### For Faster Responses:

1. **Use llama3.2 instead of llama2**
```bash
ollama pull llama3.2
# Update rag_engine.py: llm_model="llama3.2"
```

2. **Reduce top_k**
```python
# Retrieve fewer chunks (faster but less context)
response = requests.post(url, json={'query': q, 'top_k': 2})
```

3. **Optimize chunk size**
```python
# In app.py
CHUNK_SIZE = 300  # Smaller chunks = faster search
```

### For Better Accuracy:

1. **Increase top_k**
```python
# More context for better answers
{'query': question, 'top_k': 5}
```

2. **Use larger model**
```bash
ollama pull mistral  # Better quality
```

3. **Adjust chunk overlap**
```python
# In app.py
CHUNK_OVERLAP = 100  # More overlap = better context
```

## 🎯 Use Cases

- 📚 **Document Q&A** - Ask questions about PDFs
- 📖 **Research Assistant** - Query research papers
- 📋 **Legal Documents** - Search contracts, policies
- 📘 **Study Helper** - Learn from textbooks
- 📄 **Technical Docs** - Navigate API documentation
- 📝 **Report Analysis** - Extract insights from reports

## 🔐 Security Notes

- ⚠️ This is a **local application** - data stays on your machine
- ⚠️ No authentication implemented - add auth for production
- ⚠️ Validate PDF files before upload
- ⚠️ Consider rate limiting for production use

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Support for more file formats (DOCX, TXT, HTML)
- [ ] OCR for scanned PDFs
- [ ] Multi-language support
- [ ] Advanced chunking strategies
- [ ] User authentication
- [ ] Chat history
- [ ] Streaming responses
- [ ] Web UI

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [FAISS](https://github.com/facebookresearch/faiss) - Facebook Research
- [Sentence Transformers](https://www.sbert.net/) - UKPLab
- [Ollama](https://ollama.com/) - Local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

## 📞 Support

If you encounter issues:

1. ✅ Check the **Troubleshooting** section
2. ✅ Verify all dependencies are installed
3. ✅ Ensure Ollama is running: `ollama serve`
4. ✅ Check terminal logs for errors
5. ✅ Try with a smaller PDF first

## 🎓 Learn More

- [RAG Concepts](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [FAISS Documentation](https://faiss.ai/)
- [Ollama Models](https://ollama.com/library)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

**Built with ❤️ for learning RAG applications**

**Star ⭐ this repo if you found it helpful!**