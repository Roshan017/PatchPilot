
import pytest

from patchpilot.tools.reading import read_file
from patchpilot.tools.searching import list_files, search_code


@pytest.fixture
def sample_repo(tmp_path):
    repo = tmp_path / "sample-repo"
    repo.mkdir()

    (repo / "auth.py").write_text(
        "def login(password):\n"
        "    return password\n"
        "raise RuntimeError('invalid password')\n",
        encoding="utf-8",
    )

    return repo


def test_list_files(sample_repo):
    files = list_files(str(sample_repo))

    assert files == ["auth.py"]


def test_search_code_finds_matching_lines(sample_repo):
    results = search_code(str(sample_repo), "password")

    assert len(results) == 3
    assert any("auth.py:1:" in item for item in results)
    assert any("auth.py:2:" in item for item in results)
    assert any("auth.py:3:" in item for item in results)


def test_search_code_rejects_empty_keyword(sample_repo):
    with pytest.raises(ValueError, match="Keyword cannot be empty"):
        search_code(str(sample_repo), "  ")


def test_read_file_returns_contents(sample_repo):
    content = read_file(str(sample_repo), "auth.py")

    assert "def login(password)" in content
    assert "RuntimeError" in content


def test_read_file_blocks_path_traversal(sample_repo):
    with pytest.raises(ValueError, match="inside the repository"):
        read_file(str(sample_repo), "../outside.py")


def test_list_files_rejects_missing_repository(tmp_path):
    with pytest.raises(ValueError, match="Repository directory not found"):
        list_files(str(tmp_path / "missing"))


def test_list_files_ignores_virtual_environment(sample_repo):
    ignored_dir = sample_repo / ".venv"
    ignored_dir.mkdir()

    (ignored_dir / "secret.py").write_text(
        "password = 'example'",
        encoding="utf-8",
    )

    files = list_files(str(sample_repo))

    assert files == ["auth.py"]
