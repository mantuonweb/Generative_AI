#!/usr/bin/env python3
"""
Simple CLI tool to test the RAG application
"""

import requests
import sys
import os

BASE_URL = "http://localhost:8000"

def upload_pdf(filepath):
    """Upload a PDF file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    if not filepath.lower().endswith('.pdf'):
        print("❌ Only PDF files are supported")
        return
    
    print(f"📄 Uploading {filepath}...")
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/upload-pdf", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def query_rag(question, top_k=3):
    """Query the RAG system"""
    print(f"\n🔍 Question: {question}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={'query': question, 'top_k': top_k}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("💡 Answer:")
            print("-" * 80)
            print(result['answer'])
            print("-" * 80)
            
            print(f"\n📚 Used {result['num_sources']} sources\n")
            
            print("📖 Sources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"\n[{i}] {source[:200]}...")
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def get_stats():
    """Get system statistics"""
    try:
        response = requests.get(f"{BASE_URL}/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print("\n📊 Stats:")
            print(f"   Total chunks: {stats['total_chunks']}")
            print(f"   Total documents: {stats['total_documents']}")
            print(f"   Index size: {stats['index_size']}\n")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def clear_data():
    """Clear all data"""
    confirm = input("⚠️  Are you sure you want to clear all data? (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            response = requests.delete(f"{BASE_URL}/clear")
            
            if response.status_code == 200:
                print("✅ All data cleared")
            else:
                print(f"❌ Failed to clear data: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Cancelled")

def print_usage():
    """Print usage instructions"""
    print("""
🤖 RAG Application Test CLI

Usage:
    python3 test.py upload <pdf_file>       Upload a PDF
    python3 test.py query "<question>"      Ask a question
    python3 test.py stats                   Show statistics
    python3 test.py clear                   Clear all data

Examples:
    python3 test.py upload document.pdf
    python3 test.py query "What is AI?"
    python3 test.py stats
    python3 test.py clear
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "upload":
        if len(sys.argv) < 3:
            print("❌ Please provide a PDF file path")
            print("Usage: python3 test.py upload <pdf_file>")
            return
        upload_pdf(sys.argv[2])
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("❌ Please provide a question")
            print('Usage: python3 test.py query "Your question"')
            return
        question = " ".join(sys.argv[2:])
        query_rag(question)
    
    elif command == "stats":
        get_stats()
    
    elif command == "clear":
        clear_data()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()