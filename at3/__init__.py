_file_extensions = [".ttt", ".c4"]

def valid_file_extension(path: str) -> bool:
    """Returns True if the path has a valid AT3 extension"""
    for ext in _file_extensions:
        if path.endswith(ext):
            return True

    return False
