import pytest
from patchpilot.analyzer import analyze_bug
from patchpilot.context import AgentContext


def test_analyzer_finds_matching_code(tmp_path):

    repo = tmp_path / "sample-repo"
    repo.mkdir()


    (repo / "auth.py").write_text(

        "def login(password):\n"
        " raise RuntimeError('invalid password')\n",
        encoding = "utf-8"
    )


    context = AgentContext(
        bug_report="Login Password RuntimeError",
        repository_path=str(repo)
    )

    result = analyze_bug(context)

    assert "auth.py: 1" in result
    assert "auth.py: 2" in result
    assert "Files inspected: 1" in result


def test_analyzer_rejects_empty_bug_report(tmp_path):
    context = AgentContext(
        bug_report= "  ",
        repository_path= str(tmp_path),
    )

    with pytest.raises(ValueError, match = "Bug Report cannot be empty"):
        analyze_bug(context)



def test_analyzer_rejects_missisng_repo(tmp_path):

    context = AgentContext(
        bug_report= "Login Password error",
        repository_path= str(tmp_path / "missing"),
    )

    with pytest.raises(ValueError, match = "Repository directory not found"):
        analyze_bug(context)


def test_analyzer_ignores_virtual_environment(tmp_path):
    repository = tmp_path / "sample-repo"
    ignored = repository / ".venv" / "Lib"
    ignored.mkdir(parents=True)

    (ignored / "auth.py").write_text(
        "def login(password): pass",
        encoding="utf-8",
    )

    context = AgentContext(
        bug_report="Login password",
        repository_path=str(repository),
    )

    result = analyze_bug(context)

    assert "Files inspected: 0" in result
    assert "No matching source lines found." in result
