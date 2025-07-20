import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_function import available_functions, call_function

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
        verbose = sys.argv[2] == "--verbose"
    except IndexError:
        verbose = False

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response_object = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
        )

    response_text = response_object.text
    prompt_tokens = response_object.usage_metadata.prompt_token_count
    response_tokens = response_object.usage_metadata.candidates_token_count

    
    if verbose:
        print("User prompt:", prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)
    
    if not response_object.function_calls:
        print(response_text)

    for function_call_part in response_object.function_calls:
        # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, verbose)
        
        try:
            if function_call_result.parts[0].function_response.response and verbose:
                print(f"-> {function_call_result.parts[0].function_response.response["result"]}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
