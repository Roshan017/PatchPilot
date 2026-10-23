from pathlib import Path

SOURCE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".go", ".rs",
}

IGNORED_DIRS = {
    ".git", ".venv", "venv",
    "__pycache__", "node_modules",
    ".pytest_cache",
}


def read_file(repository_path: str, relative_path: str) -> str:

    """ Read a source file located inside the repository."""

    repository = Path(repository_path).resolve()
    target  = (repository / relative_path).resolve()

    if not repository.is_dir():
        raise ValueError(f"repository not found: {repository}")

    if not target.is_relative_to(repository):
        raise ValueError(
            "File path must remain inside the repository"
        )
    if not target.is_file():
        raise ValueError(f"File not found: {relative_path}")
    
    if target.suffix.lower() not in SOURCE_EXTENSIONS:
        raise ValueError("Unsupported source-file type")
    
    if any(part in IGNORED_DIRS for part in target.parts):
        raise ValueError("Cannot read files in ignored directories")


    return target.read_text(encoding="utf-8", errors="replace")