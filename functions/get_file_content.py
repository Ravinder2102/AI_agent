import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_absolute, file_path))

        valid_file_path = os.path.commonpath([working_dir_absolute, target_file_path]) == working_dir_absolute

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file_path, "r") as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
