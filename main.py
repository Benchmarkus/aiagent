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

    if verbose:
        print("User prompt:", prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(MAX_ITERATIONS):
        try:
            response = generate_content(client, messages, verbose)

            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if response.function_calls:
                function_responses = execute_functions(response, verbose)
                tool_message = types.Content(role="tool", parts=function_responses)
                messages.append(tool_message)
            else:
                print(response.text)
                break
            
        except Exception as e:
            print("Error in loop:", e)


def generate_content(client, messages, verbose):    

    response_object = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
        )

    prompt_tokens = response_object.usage_metadata.prompt_token_count
    response_tokens = response_object.usage_metadata.candidates_token_count
    
    if verbose:
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)
    
    return response_object
    
def execute_functions(response_object, verbose=False):

    function_responses = []
    for function_call_part in response_object.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        try:
            if function_call_result.parts[0].function_response.response and verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except Exception as e:
            print(f"Error@222: {e}")
            sys.exit(1)
        
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    return function_responses

if __name__ == "__main__":
    main()
