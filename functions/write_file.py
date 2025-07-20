import os
from google.genai import types

def write_file(working_directory, filepath, content):
    combined_path = os.path.join(working_directory, filepath)
    combined_path_abs = os.path.abspath(combined_path)

    working_directory_abs = os.path.abspath(working_directory)

    if not combined_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{filepath}" as it is outside the permitted working directory'

    directory_path_only = os.path.dirname(combined_path)
    if not os.path.exists(directory_path_only):
        try:
            os.makedirs(directory_path_only)
        except Exception as e:
            return f"Error: {e}"

    try:
        with open(combined_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{filepath}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to an existing file or create a new file if it doesn't exist. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The file to be written on.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents in str to be written on to the file.",
            ),
        },
    ),
)
