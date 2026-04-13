import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_absolute,file_path))

        valid_file_path = os.path.commonpath([target_file_path, working_dir_absolute]) == working_dir_absolute

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, text=True, timeout=30,capture_output=True, cwd=working_dir_absolute)
        
        result_string = []
        if result.returncode != 0:
            result_string.append(f"Process exited with code {result.returncode}")
        if not result.stdout == 0 and not result.stderr:
            result_string.append("No output produced")
        
        if result.stdout:
            result_string.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            result_string.append(f"STDERR:\n{result.stderr}")
        return "\n".join(result_string) 

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
             "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script"
            ),
        },
    ),
)