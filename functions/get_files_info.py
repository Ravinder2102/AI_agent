import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_absolute, directory))

        valid_dir = os.path.commonpath([working_dir_absolute, target_dir]) == working_dir_absolute

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_files_list = os.listdir(target_dir)
        report = []
        for file_name in dir_files_list:
            filepath = os.path.join(target_dir,file_name)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            report.append(
                f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(report)
    except Exception as e:
        return f"Error listing files: {e}"
    

