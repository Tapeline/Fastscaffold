from pathlib import Path


def save_files(root: str, files: dict[str, str]) -> None:
    for filename, contents in files.items():
        path = Path(root, filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        if filename.endswith(".py"):
            Path(path.parent, "__init__.py").write_text("")
