import os
import subprocess

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