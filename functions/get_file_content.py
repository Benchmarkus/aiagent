import os
from config import *
from google import genai
from google.genai import types

def get_file_content(working_directory, filepath):

    combined_path = os.path.join(working_directory, filepath)
    combined_path_abs = os.path.abspath(combined_path)

    working_directory_abs = os.path.abspath(working_directory)

    if not combined_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot read "{filepath}" as it is outside the permitted working directory'

    if not os.path.isfile(combined_path):
        return f'Error: File not found or is not a regular file: "{filepath}"'
    
    with open(combined_path, "r") as file:
        
        content = file.read()
        
        if len(content) > MAX_CHAR:
            over_max_char = f'[...File "{filepath}" truncated at {MAX_CHAR} characters]'
            result = content[:MAX_CHAR] + "\n" + over_max_char
        else: 
            result = content

    return result

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string that is the contents of the called file, constrained to the working directory. If file size is over 10000 characters, the output is truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The file whose content is to be returned by the function. For example 'main.py'.",
            ),
        },
    ),
)