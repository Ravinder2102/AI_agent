import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_absolute, file_path))

        valid_file_path = working_dir_absolute == os.path.commonpath([working_dir_absolute, target_file_path])

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"