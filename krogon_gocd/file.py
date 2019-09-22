import os
from typing import Optional


def cwd() -> str:
    return os.getcwd()


def write(file_path: str, content: str, flags: Optional[str] = 'w') -> None:
    with open(file_path, flags) as file:
        file.write(content)


def read(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()


def path_rel_to_file(file_path: str, file_name: str) -> str:
    return os.path.dirname(os.path.abspath(file_name)) + '/' + file_path


def path_rel_to_cwd(file_path: str):
    return os.path.abspath(cwd() + '/' + file_path)
