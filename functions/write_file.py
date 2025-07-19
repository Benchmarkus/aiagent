import os

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

