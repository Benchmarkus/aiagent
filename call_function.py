from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def call_function(function_call_part, verbose=False):

    function_call_part.args["working_directory"] = WORKING_DIRECTORY

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == "get_files_info":
        result_of_call = get_files_info(**function_call_part.args)

    elif function_call_part.name == "get_file_content":
        result_of_call = get_file_content(**function_call_part.args)

    elif function_call_part.name == "run_python_file":
        result_of_call = run_python_file(**function_call_part.args)

    elif function_call_part.name == "write_file":
        result_of_call = write_file(**function_call_part.args)

    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result_of_call},
            )
        ],
    )