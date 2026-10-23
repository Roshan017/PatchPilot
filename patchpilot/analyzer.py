from importlib.resources import read_text
from signal import raise_signal
from patchpilot.context import AgentContext
import re
from pathlib import Path

from patchpilot.context import AgentContext

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
}

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
}

STOP_WORDS = {
    "this", "that", "with", "from", "when", "where",
    "what", "into", "then", "than", "have", "does",
    "should", "could", "would", "error", "fails",
    "failure", "broken", "issue", "bug", "code",
}


def extract_keywords(bug_report: str) -> list[str]:

    """
    Extract simple search terms from a bug report.
    """

    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9]*", bug_report.lower())

    return list(dict.fromkeys(word for word in words if len(word) >= 4 and word not in STOP_WORDS))



def discover_Files(repository: Path) -> list[Path]:

    """ Find supported source files, skipping irrelavant directories"""

    files  = []

    for path in repository.rglob("*"):

        if not path.is_file():
            continue

        if any (part in IGNORED_DIRS for part in path.parts):
            continue

        if path.suffix.lower() in SOURCE_EXTENSIONS:
            files.append(path)
        
    return sorted(files)


def analyze_bug(context: AgentContext) -> str:

    """
    Inspect repo source files and collect matching evidence 
    """

    if not context.bug_report.strip():
        raise ValueError("Bug Report cannot be empty")

    repository = Path(context.repository_path).resolve()

    if not repository.is_dir():
        raise ValueError(
            f"Repository directory not found: {repository}"
        )

    keywords = extract_keywords(context.bug_report)

    if not keywords:
        raise ValueError(
            "Bug Report does not contain searchable keywords"
        )
    
    files = discover_Files(repository)

    findings = []

    for file_path in files:

        try: 
            content = file_path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except OSError:
            continue


        for line_number, line in enumerate(
            content.splitlines(), start=1
        ):
            matched = [

                keyword for keyword in keywords
                    if re.search(
                        rf"(?<!\w){re.escape(keyword)}(?!\w)", line , re.IGNORECASE
                    )
            ]

            if matched:
                relative_path = file_path.relative_to(repository)

                findings.append(
                    f"{relative_path}: {line_number}: "
                    f"[{', '.join(matched)}] {line.strip()}"
                )
        
    if not findings:
        findings_summary = "No matching source lines found."
    else:
        findings_summary = "\n".join(findings[:50])

    return (
        f"Bug Report: {context.bug_report}\n"
        f"Repository: {repository}\n"
        f"Files inspected: {len(files)}\n"
        f"Keywords: {','.join(keywords)}\n"
        f"Findings:\n{findings_summary}"
    )




# def analyze_bug(context: AgentContext) -> str:
#     """
#     Produce a placeholder investigation for the supplied bug report.
#     """

#     if not context.bug_report.strip():
#         raise ValueError("Bug report cannot be empty")


#     return (
#         f"Investigation started for : {context.bug_report}"
#         f"Repository: {context.repository_path}"
#     )