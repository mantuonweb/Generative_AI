# 🚀 Quick Setup Guide

Simple step-by-step guide to get your RAG application running in 5 minutes.

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Download from [ollama.com/download](https://ollama.com/download)

### Step 2: Pull AI Model

```bash
ollama pull llama2
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Start Everything

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

**Terminal 2 - Start RAG App:**
```bash
python3 app.py
```

**Terminal 3 - Upload & Query:**
```bash
python3 create_sample_pdf.py
python3 test.py upload sample.pdf
python3 test.py query "What is AI?"
```

Done! 🎉

---

## 📝 Basic Commands

### Upload a PDF
```bash
python3 test.py upload your_document.pdf
```

### Ask Questions
```bash
python3 test.py query "Your question here?"
```

### Check Stats
```bash
python3 test.py stats
```

### Clear All Data
```bash
python3 test.py clear
```

### Interactive Mode
```bash
python3 interactive_query.py
```

---

## 🔧 Common Issues

### "Cannot connect to Ollama"
```bash
# Start Ollama in another terminal
ollama serve
```

### "Model not found"
```bash
ollama pull llama2
```

### "Port already in use"
```bash
# Kill existing process
pkill -f "python3 app.py"
# Then restart
python3 app.py
```

### "Module not found"
```bash
pip3 install -r requirements.txt
```

---

## 🌐 Using the Web Interface

Open browser: `http://localhost:8000/docs`

- Interactive API documentation
- Test all endpoints
- No command line needed

---

## 🛑 Stop Everything

```bash
# Press Ctrl+C in each terminal
# Or kill all processes:
pkill ollama
pkill -f "python3 app.py"
```

---

## 💡 Tips

**Faster responses?** Use llama3.2:
```bash
ollama pull llama3.2
# Edit rag_engine.py: llm_model="llama3.2"
```

**Better answers?** Increase sources:
```bash
python3 test.py query "question" --top_k 5
```

**Check if working?**
```bash
curl http://localhost:8000/stats
```

---

## 📞 Need Help?

1. Check Ollama is running: `ollama list`
2. Check app is running: `curl http://localhost:8000`
3. Check logs in the terminal windows
4. Try with sample PDF first: `python3 create_sample_pdf.py`

---

**That's it! Keep it simple. 🚀**