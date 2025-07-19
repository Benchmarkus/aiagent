import os
import sys
from dotenv import load_dotenv
from google import genai

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        prompt = sys.argv[1]
    except IndexError:
        print("ERROR: No prompt inserted")
        sys.exit(1)

    response_object = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)

    response_text = response_object.text
    prompt_tokens = response_object.usage_metadata.prompt_token_count
    response_tokens = response_object.usage_metadata.candidates_token_count

    print(response_text)
    print("Prompt tokens:", prompt_tokens)
    print("Response tokens:", response_tokens)


if __name__ == "__main__":
    main()
