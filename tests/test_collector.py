import pytest
from pilepack.collector import collect_files, build_tree
from pathlib import Path

def test_collect_files_respect_gitignore(test_project):
    (test_project / ".gitignore").write_text("utils/\n")
    files = collect_files(test_project, follow_gitignore=True)
    rel_paths = [str(p) for p in files]
    assert "utils/helpers.py" not in rel_paths
    assert "main.py" in rel_paths

def test_collect_files_ignore_gitignore(test_project):
    (test_project / ".gitignore").write_text("main.py")
    files = collect_files(test_project, follow_gitignore=False)
    rel_paths = [str(p) for p in files]
    assert "main.py" in rel_paths

def test_collect_files_excludes_git_and_gitignore(test_project):
    (test_project / ".git").mkdir()
    (test_project / ".git" / "config").touch()
    (test_project / ".gitignore").touch()
    files = collect_files(test_project, follow_gitignore=False)
    rel_paths = [str(p) for p in files]
    assert ".git" not in rel_paths
    assert ".gitignore" not in rel_paths
    assert "main.py" in rel_paths

def test_collect_files_skips_symlinks_by_default(test_project, tmp_path):
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("outside")
    link = test_project / "linked-outside.txt"
    try:
        link.symlink_to(outside_file)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not supported here: {exc}")

    files = collect_files(test_project, follow_gitignore=False)
    rel_paths = [str(p) for p in files]

    assert "linked-outside.txt" not in rel_paths

def test_collect_files_can_follow_symlinks_when_requested(test_project, tmp_path):
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("outside")
    link = test_project / "linked-outside.txt"
    try:
        link.symlink_to(outside_file)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not supported here: {exc}")

    files = collect_files(test_project, follow_gitignore=False, follow_symlinks=True)
    rel_paths = [str(p) for p in files]

    assert "linked-outside.txt" in rel_paths

def test_build_tree():
    files = [Path("a/b/c.py"), Path("a/d.py"), Path("e.py")]
    tree = build_tree(files)
    expected = {"a": {"b": {"c.py": None}, "d.py": None}, "e.py": None}
    assert tree == expected
