import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_function import available_functions

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        prompt = sys.argv[1]
    except IndexError:
        print("ERROR: No prompt inserted")
        sys.exit(1)
    
    try:
        is_verbose = sys.argv[2] == "--verbose"
    except IndexError:
        is_verbose = False

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response_object = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
        )

    response_text = response_object.text
    prompt_tokens = response_object.usage_metadata.prompt_token_count
    response_tokens = response_object.usage_metadata.candidates_token_count

    
    if is_verbose:
        print("User prompt:", prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)
    
    if len(response_object.function_calls) != 0:
        print(f"Calling function: {response_object.function_calls[0].name}({response_object.function_calls[0].args})")
    else:
        print(response_text)


if __name__ == "__main__":
    main()
