import argparse
import ollama

def get_bot_response(question):
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': question}])
    bot_response = response['message']['content']
    return bot_response

def chunk_response(response, chunk_size=80):
    # Chunk the response into smaller parts
    return [response[i:i+chunk_size] for i in range(0, len(response), chunk_size)]

def main():
    parser = argparse.ArgumentParser(description="Chat with an AI bot")
    parser.add_argument("question", type=str, help="Your question to the bot")
    args = parser.parse_args()

    question = args.question

    bot_response = get_bot_response(question)
    chunks = chunk_response(bot_response)

    print("Bot's Response:")
    for chunk in chunks:
        print(chunk)

if __name__ == "__main__":
    main()
