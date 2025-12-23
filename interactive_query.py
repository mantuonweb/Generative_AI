import requests
import sys

BASE_URL = "http://localhost:8000"

def query_rag(question, top_k=3):
    """Ask a question with formatted output"""
    print("\n" + "="*80)
    print(f"🔍 QUESTION: {question}")
    print("="*80)
    
    response = requests.post(
        f"{BASE_URL}/query",
        json={'query': question, 'top_k': top_k}
    )
    result = response.json()
    
    print(f"\n💡 ANSWER:")
    print("-"*80)
    print(result['answer'])
    
    print(f"\n📚 SOURCES USED: {result['num_sources']}")
    print("-"*80)
    for i, source in enumerate(result['sources'], 1):
        print(f"\n[Source {i}]")
        print(source)
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Interactive mode
        print("🤖 RAG Interactive Query Mode")
        print("Type 'exit' to quit\n")
        
        while True:
            question = input("❓ Your question: ")
            if question.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            if question.strip():
                query_rag(question)
    else:
        # Command line mode
        question = " ".join(sys.argv[1:])
        query_rag(question)