from pathlib import Path

from patchpilot.tools.reading import(
    IGNORED_DIRS, SOURCE_EXTENSIONS
)


def list_files(repository_path: str) -> list[str]:
    """ List Source files in a repository. """

    repository = Path(repository_path).resolve()


    if not repository.is_dir():
        raise ValueError("Repository directory not found")

    
    files = []

    for path in repository.rglob("*"):

        if not path.is_file():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        if path.suffix.lower() in SOURCE_EXTENSIONS:
            files.append(str(path.relative_to(repository)))
        

    return sorted(files)



def search_code(
    repository_path: str,
    keyword: str,
) -> list[str]:
    """Search source files for a keyword."""

    if not keyword.strip():
        raise ValueError("Keyword cannot be empty")

    repository = Path(repository_path).resolve()
    files = list_files(str(repository))
    findings = []

    for relative_path in files:
        file_path = repository / relative_path

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            continue

        for line_number, line in enumerate(
            content.splitlines(), start=1
        ):
            if keyword.casefold() in line.casefold():
                findings.append(
                    f"{relative_path}:{line_number}: {line.strip()}"
                )

    return findings[:100]
