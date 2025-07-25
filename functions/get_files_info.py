import os
from google import genai
from google.genai import types
from config import *

def get_files_info(working_directory, directory="."):

    combined_path = os.path.join(working_directory, directory)
    combined_path_abs = os.path.abspath(combined_path)

    working_directory_abs = os.path.abspath(working_directory)

    if not combined_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isfile(directory):
        return f'Error: "{directory}" is not a directory'
    
    result = []
    for f in os.listdir(combined_path):
        is_dir = not os.path.isfile(f)
        size = os.path.getsize(os.path.join(combined_path, f))
        result.append(f"- {f}: file_size={size} bytes, is_dir={is_dir}")
    
    if directory == ".":
        header = f"Result for current directory:"
    else:
        header = f"Result for '{directory}' directory:"

    return header + "\n" + "\n".join(result)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
