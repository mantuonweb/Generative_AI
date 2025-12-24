# RAG Engine Documentation

Complete documentation for the `RAGEngine` class - a Retrieval-Augmented Generation system using FAISS and Ollama.

---

## Table of Contents

1. [Overview](#overview)
2. [Class: RAGEngine](#class-ragengine)
3. [Methods](#methods)
4. [Usage Examples](#usage-examples)
5. [Understanding Key Concepts](#understanding-key-concepts)
6. [Comparison with TypeScript/JavaScript](#comparison-with-typescriptjavascript)

---

## Overview

The `RAGEngine` class implements a Retrieval-Augmented Generation (RAG) system that:
- Stores document chunks as vector embeddings using FAISS
- Retrieves relevant context based on user queries
- Generates answers using a local LLM (Ollama)

### Key Features
- ✅ Vector similarity search with FAISS
- ✅ Sentence embeddings with SentenceTransformer
- ✅ Local LLM integration with Ollama
- ✅ Persistent storage (save/load state)
- ✅ Customizable prompt templates

---

## Class: RAGEngine

### Initialization

```python
class RAGEngine:
    """Retrieval-Augmented Generation engine using FAISS and Ollama.
    
    Attributes:
        embedding_model: SentenceTransformer for creating embeddings
        llm_model: Name of the Ollama model to use
        dimension: Embedding vector dimension (384 for all-MiniLM-L6-v2)
        index: FAISS index for vector similarity search
        chunks: List of document text chunks
        metadata: List of metadata dictionaries for each chunk
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2", llm_model="llama3.2"):
        """Initialize the RAG engine.
        
        Args:
            model_name: Name of the sentence transformer model (default: "all-MiniLM-L6-v2")
            llm_model: Name of the Ollama LLM model (default: "llama3.2")
        """
```

**Example:**
```python
# Default initialization
rag = RAGEngine()

# Custom models
rag = RAGEngine(
    model_name="paraphrase-MiniLM-L6-v2",
    llm_model="mistral"
)
```

---

## Methods

### 1. `add_document()`

Add a document chunk to the FAISS vector store.

```python
def add_document(self, doc_id: str, content: str, filename: str):
    """Add a document chunk to FAISS vector store.
    
    Args:
        doc_id: Unique identifier for the document chunk
        content: Text content of the chunk
        filename: Source filename for reference
        
    Returns:
        None
        
    Side Effects:
        - Generates embedding for the content
        - Adds embedding to FAISS index
        - Stores chunk text and metadata
    """
```

**Example:**
```python
rag.add_document(
    doc_id="doc1_chunk1",
    content="Python is a high-level programming language...",
    filename="python_guide.txt"
)
```

**What Happens:**
1. Content is converted to a 384-dimensional vector embedding
2. Vector is added to FAISS index
3. Original text and metadata are stored for retrieval

---

### 2. `search()`

Search for relevant document chunks based on a query.

```python
def search(self, query: str, top_k: int = 3) -> List[Dict]:
    """Search for relevant chunks based on query.
    
    Args:
        query: Search query string
        top_k: Number of most relevant results to return (default: 3)
        
    Returns:
        List of dictionaries, each containing:
            - id: Document chunk ID
            - filename: Source filename
            - content: Chunk text
            - score: Similarity score (0-1, higher is better)
            
    Example:
        >>> results = rag.search("What is Python?", top_k=3)
        >>> print(results[0]['content'])
        Python is a high-level programming language...
    """
```

**Example:**
```python
results = rag.search("What is machine learning?", top_k=5)

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Source: {result['filename']}")
    print(f"Content: {result['content'][:100]}...")
    print("---")
```

**Output:**
```
Score: 0.85
Source: ml_guide.txt
Content: Machine learning is a subset of artificial intelligence that enables computers to learn...
---
Score: 0.78
Source: ai_basics.txt
Content: ML algorithms use statistical techniques to find patterns in data...
---
```

---

### 3. `create_prompt()`

Create a formatted prompt for the LLM from query and context.

```python
def create_prompt(self, query: str, context: str, prompt_template: str = None) -> str:
    """Create a prompt for the LLM from query and context.
    
    Args:
        query: User's question
        context: Retrieved document chunks (concatenated)
        prompt_template: Optional custom template with {context} and {query} placeholders
        
    Returns:
        Formatted prompt string ready for LLM
        
    Example:
        >>> context = "Python is a programming language..."
        >>> query = "What is Python?"
        >>> prompt = rag.create_prompt(query, context)
        >>> print(prompt)
        Based on the following context, answer the question.
        
        Context:
        Python is a programming language...
        
        Question: What is Python?
        
        Answer:
    """
```

**Example with Default Template:**
```python
context = "Python is a high-level programming language known for readability."
query = "What is Python?"
prompt = rag.create_prompt(query, context)
```

**Example with Custom Template:**
```python
custom_template = """You are a technical expert.

CONTEXT: {context}

USER QUESTION: {query}

EXPERT ANSWER:"""

prompt = rag.create_prompt(query, context, custom_template)
```

---

### 4. `generate_answer()`

Generate an answer using Retrieval-Augmented Generation.

```python
def generate_answer(self, query: str, top_k: int = 3) -> Dict:
    """Generate answer using RAG.
    
    This is the main method that orchestrates the entire RAG pipeline:
    1. Search for relevant document chunks
    2. Build context from retrieved chunks
    3. Create a prompt with context and query
    4. Generate answer using LLM
    
    Args:
        query: User's question
        top_k: Number of relevant chunks to retrieve (default: 3)
        
    Returns:
        Dictionary containing:
            - answer: Generated answer from LLM
            - sources: List of source text previews (first 200 chars)
            - num_sources: Number of sources used
            
    Example:
        >>> result = rag.generate_answer("What is Python?", top_k=3)
        >>> print(result['answer'])
        Python is a high-level programming language...
        >>> print(f"Used {result['num_sources']} sources")
        Used 3 sources
    """
```

**Complete Flow:**

```
User Query: "What is Python?"
         ↓
    [1. Search]
         ↓
    Convert query to embedding
         ↓
    FAISS finds 3 similar chunks
         ↓
    [2. Check if empty]
         ↓
    [3. Build context]
         ↓
    Combine all chunk texts
         ↓
    [4. Create prompt]
         ↓
    Format: Context + Question
         ↓
    [5. LLM Generation]
         ↓
    Send to Ollama → Get answer
         ↓
    [6. Return result]
         ↓
    {answer, sources, num_sources}
```

**Example:**
```python
result = rag.generate_answer("What is machine learning?", top_k=3)

print("Answer:", result['answer'])
print("\nSources used:", result['num_sources'])
print("\nSource previews:")
for i, source in enumerate(result['sources'], 1):
    print(f"{i}. {source}")
```

**Output:**
```
Answer: Machine learning is a subset of artificial intelligence that enables 
computers to learn from data without being explicitly programmed. It uses 
statistical techniques to identify patterns and make predictions.

Sources used: 3

Source previews:
1. Machine learning is a subset of artificial intelligence that enables computers 
   to learn from data. It involves algorithms that improve automatically through...
2. ML algorithms can be categorized into supervised learning, unsupervised learning, 
   and reinforcement learning. Each type serves different purposes...
3. Common applications of machine learning include image recognition, natural 
   language processing, recommendation systems, and predictive analytics...
```

---

### 5. `get_all_documents()`

Retrieve all stored document chunks.

```python
def get_all_documents(self) -> List[Dict]:
    """Get all stored chunks.
    
    Returns:
        List of dictionaries, each containing:
            - id: Document chunk ID
            - filename: Source filename
            - content: Full chunk text
            
    Example:
        >>> docs = rag.get_all_documents()
        >>> print(f"Total chunks: {len(docs)}")
        Total chunks: 42
    """
```

**Example:**
```python
all_docs = rag.get_all_documents()

for doc in all_docs[:3]:  # Show first 3
    print(f"ID: {doc['id']}")
    print(f"File: {doc['filename']}")
    print(f"Content: {doc['content'][:100]}...")
    print("---")
```

---

### 6. `save_state()`

Save FAISS index and data to disk for persistence.

```python
def save_state(self, filepath: str = "data/rag_state.pkl"):
    """Save FAISS index and data to disk.
    
    Args:
        filepath: Path to save the state file (default: "data/rag_state.pkl")
        
    Side Effects:
        - Creates directory if it doesn't exist
        - Saves FAISS index to .faiss file
        - Saves chunks and metadata to .pkl file
        
    Example:
        >>> rag.save_state("data/my_rag.pkl")
        💾 Saved state to data/my_rag.pkl
    """
```

**Example:**
```python
# Save with default path
rag.save_state()

# Save with custom path
rag.save_state("backups/rag_backup_2024.pkl")
```

**Files Created:**
- `data/rag_state.pkl` - Chunks and metadata (pickle format)
- `data/rag_state.faiss` - FAISS vector index

---

### 7. `load_state()`

Load FAISS index and data from disk.

```python
def load_state(self, filepath: str = "data/rag_state.pkl") -> bool:
    """Load FAISS index and data from disk.
    
    Args:
        filepath: Path to the state file (default: "data/rag_state.pkl")
        
    Returns:
        True if successfully loaded, False if files don't exist
        
    Example:
        >>> if rag.load_state():
        ...     print("State loaded successfully")
        ... else:
        ...     print("No saved state found")
        📂 Loaded 42 chunks from data/rag_state.pkl
        State loaded successfully
    """
```

**Example:**
```python
# Create new RAG instance
rag = RAGEngine()

# Load previous state
if rag.load_state("data/rag_state.pkl"):
    print("Loaded existing data")
    result = rag.generate_answer("What is Python?")
else:
    print("No saved data, starting fresh")
```

---

### 8. `clear()`

Clear all stored data and reset the index.

```python
def clear(self):
    """Clear all data.
    
    Side Effects:
        - Resets FAISS index to empty state
        - Clears all chunks
        - Clears all metadata
        
    Example:
        >>> rag.clear()
        🗑️ Cleared all data
    """
```

**Example:**
```python
# Clear everything
rag.clear()

# Verify it's empty
print(f"Chunks remaining: {len(rag.chunks)}")  # Output: 0
```

---

## Usage Examples

### Complete Workflow Example

```python
from rag_engine import RAGEngine

# 1. Initialize
rag = RAGEngine()

# 2. Add documents
documents = [
    {
        'id': 'doc1_chunk1',
        'content': 'Python is a high-level programming language known for its readability.',
        'filename': 'python_intro.txt'
    },
    {
        'id': 'doc1_chunk2',
        'content': 'Python supports multiple programming paradigms including OOP and functional.',
        'filename': 'python_intro.txt'
    },
    {
        'id': 'doc2_chunk1',
        'content': 'Machine learning is a subset of AI that learns from data.',
        'filename': 'ml_basics.txt'
    }
]

for doc in documents:
    rag.add_document(doc['id'], doc['content'], doc['filename'])

# 3. Search for relevant content
results = rag.search("What is Python?", top_k=2)
print("Search Results:")
for r in results:
    print(f"- {r['content']} (score: {r['score']:.2f})")

# 4. Generate answer
result = rag.generate_answer("What is Python?", top_k=2)
print("\nGenerated Answer:")
print(result['answer'])

# 5. Save state
rag.save_state()

# 6. Later... load state
new_rag = RAGEngine()
new_rag.load_state()
```

### Custom Prompt Template Example

```python
# Define custom template
technical_template = """You are a senior software engineer. 
Use the following technical documentation to answer the question precisely.

DOCUMENTATION:
{context}

QUESTION: {query}

TECHNICAL ANSWER:"""

# Use custom template
result = rag.generate_answer(
    "How does Python handle memory management?",
    top_k=3,
    prompt_template=technical_template
)
```

---

## Understanding Key Concepts

### 1. What are Placeholders?

Placeholders like `{context}` and `{query}` are **NOT comments**. They are replaced with actual values.

**Before `.format()`:**
```python
template = "Hello {name}, you are {age} years old"
```

**After `.format(name="Alice", age=25)`:**
```python
"Hello Alice, you are 25 years old"
```

### 2. What are Docstrings?

Docstrings are documentation strings that explain what functions do.

```python
def my_function(x: int) -> int:
    """This is a docstring.
    
    Args:
        x: Input number
        
    Returns:
        Double the input
    """
    return x * 2
```

**Access docstring:**
```python
print(my_function.__doc__)
help(my_function)
```

### 3. RAG Pipeline Explained

```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. INDEXING (Done Once)                               │
│     Documents → Chunks → Embeddings → FAISS Index      │
│                                                         │
│  2. RETRIEVAL (Per Query)                              │
│     Query → Embedding → Search FAISS → Top-K Chunks    │
│                                                         │
│  3. AUGMENTATION (Per Query)                           │
│     Chunks → Context → Prompt Template → Full Prompt   │
│                                                         │
│  4. GENERATION (Per Query)                             │
│     Prompt → LLM (Ollama) → Answer                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4. Vector Similarity Search

**How it works:**
1. Text is converted to numbers (embeddings): `[0.23, -0.45, 0.67, ...]`
2. Similar texts have similar embeddings
3. FAISS finds nearest neighbors in vector space

**Example:**
```
Query: "What is Python?"
Embedding: [0.2, 0.5, -0.3, ...]

Document 1: "Python is a programming language"
Embedding: [0.21, 0.48, -0.29, ...]  ← Very close! (High similarity)

Document 2: "Cats are mammals"
Embedding: [-0.5, 0.1, 0.8, ...]     ← Far away (Low similarity)
```

---

## Comparison with TypeScript/JavaScript

### Docstrings vs JSDoc

**Python Docstring:**
```python
def create_prompt(self, query: str, context: str) -> str:
    """Create a prompt for the LLM.
    
    Args:
        query: User's question
        context: Retrieved document chunks
        
    Returns:
        Formatted prompt string
    """
```

**TypeScript JSDoc:**
```typescript
/**
 * Create a prompt for the LLM
 * 
 * @param query - User's question
 * @param context - Retrieved document chunks
 * @returns Formatted prompt string
 */
function createPrompt(query: string, context: string): string {
    // function code
}
```

### String Formatting

**Python `.format()`:**
```python
template = "Hello {name}, you are {age}"
result = template.format(name="Bob", age=30)
```

**JavaScript Template Literals:**
```javascript
const name = "Bob";
const age = 30;
const result = `Hello ${name}, you are ${age}`;
```

### Class Comparison

**Python:**
```python
class RAGEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
    
    def search(self, query: str) -> List[Dict]:
        pass
```

**TypeScript:**
```typescript
class RAGEngine {
    modelName: string;
    
    constructor(modelName = "all-MiniLM-L6-v2") {
        this.modelName = modelName;
    }
    
    search(query: string): Array<Record<string, any>> {
        // implementation
    }
}
```

---

## API Reference Summary

| Method | Purpose | Returns |
|--------|---------|---------|
| `__init__()` | Initialize RAG engine | None |
| `add_document()` | Add document chunk to index | None |
| `search()` | Find relevant chunks | `List[Dict]` |
| `create_prompt()` | Format prompt for LLM | `str` |
| `generate_answer()` | Complete RAG pipeline | `Dict` |
| `get_all_documents()` | Retrieve all chunks | `List[Dict]` |
| `save_state()` | Persist to disk | None |
| `load_state()` | Load from disk | `bool` |
| `clear()` | Reset all data | None |

---

## Best Practices

### 1. Document Chunking
```python
# ✅ Good: Reasonable chunk size (200-500 words)
rag.add_document("doc1_chunk1", "Python is a high-level...", "guide.txt")

# ❌ Bad: Too large (entire book)
rag.add_document("doc1", entire_book_text, "book.txt")

# ❌ Bad: Too small (single sentence)
rag.add_document("doc1_s1", "Python is great.", "guide.txt")
```

### 2. Query Formulation
```python
# ✅ Good: Clear, specific questions
result = rag.generate_answer("What are the benefits of Python for data science?")

# ❌ Bad: Vague queries
result = rag.generate_answer("Python stuff")
```

### 3. Error Handling
```python
try:
    result = rag.generate_answer("What is AI?")
    print(result['answer'])
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

### 4. State Management
```python
# Save after adding documents
rag.add_document(...)
rag.save_state()

# Load at startup
rag = RAGEngine()
if not rag.load_state():
    # Initialize with documents
    pass
```

---

## Troubleshooting

### Common Issues

**1. "No relevant information found"**
- Check if documents were added: `len(rag.chunks)`
- Try increasing `top_k` parameter
- Verify query matches document content

**2. "Error generating answer"**
- Ensure Ollama is running: `ollama serve`
- Check model is installed: `ollama list`
- Verify model name is correct

**3. FAISS index errors**
- Ensure embeddings are same dimension
- Check FAISS is installed: `pip install faiss-cpu`

---

## Dependencies

```bash
pip install sentence-transformers
pip install faiss-cpu
pip install ollama
pip install numpy
```

---

## License

This documentation is part of the RAG Engine project.

---

**Last Updated:** 2024
**Version:** 1.0.0