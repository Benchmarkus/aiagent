import os
import subprocess
from google.genai import types

def run_python_file(working_directory, filepath, args=[]):

    combined_path = os.path.join(working_directory, filepath)
    combined_path_abs = os.path.abspath(combined_path)

    working_directory_abs = os.path.abspath(working_directory)

    if not combined_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot execute "{filepath}" as it is outside the permitted working directory'

    if not os.path.exists(combined_path):
        return f'Error: File "{filepath}" not found.'

    if not filepath.endswith(".py"):
        return f'Error: "{filepath}" is not a Python file.'

    try:
        completed_process = subprocess.run(args=(["python", filepath].__add__(args)), timeout=30, capture_output=True, cwd=working_directory, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    result = []
    result.append(f"STDOUT: {completed_process.stdout}\n")
    result.append(f"STDERR: {completed_process.stderr}\n")

    if completed_process.returncode != 0:
        result.append(f"Process exited with code {completed_process.returncode}\n")

    if len(result) == 0:
        return f"No output produced."

    return "".join(result)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python files in specified filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The python file to be ran.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Extra args. Default is empty list []",
            ),
        },
    ),
)
