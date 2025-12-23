import requests

# Query the system
response = requests.post(
    'http://localhost:8000/query',
    json={
        'query': 'What is this document about?',
        'top_k': 3
    }
)

result = response.json()

print("=" * 80)
print("ANSWER:")
print("=" * 80)
print(result['answer'])
print("\n" + "=" * 80)
print(f"SOURCES USED: {result['num_sources']}")
print("=" * 80)
for i, source in enumerate(result['sources'], 1):
    print(f"\nSource {i}:")
    print(source)