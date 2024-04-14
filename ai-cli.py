import ollama

def test_ollama_connectivity():
    try:
        chunk_size = 5  # Set the chunk size
        num_results = 20  # Set the total number of results needed
        offset = 0
        while offset < num_results:
            # Fetch results in chunks
            response = ollama.search("Hello, OLLAma!", num_results=chunk_size, offset=offset)
            print("OLLAma API connection successful.")
            print("Response (Chunk {}):".format(offset//chunk_size + 1), response)
            offset += chunk_size
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    test_ollama_connectivity()
