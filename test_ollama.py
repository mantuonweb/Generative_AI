import ollama

try:
    response = ollama.generate(
        model='llama2',
        prompt='Say hello in one sentence.'
    )
    print("✅ Ollama is working!")
    print(f"Response: {response['response']}")
except Exception as e:
    print(f"❌ Ollama error: {e}")
    print("\nMake sure:")
    print("1. Ollama is installed: ollama --version")
    print("2. Ollama is running: ollama serve")
    print("3. Model is pulled: ollama pull llama2")