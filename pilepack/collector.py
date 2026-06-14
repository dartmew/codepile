from .ignorer import load_gitignore, is_ignored
from pathlib import Path
from typing import Dict, List


def collect_files(root_path: Path, follow_gitignore: bool = True, follow_symlinks: bool = False) -> List[Path]:
    if not root_path.is_dir():
        raise NotADirectoryError(f"{root_path} does not exist or is not a directory")

    if follow_gitignore:
        spec = load_gitignore(root_path)
    else:
        spec = None
    collected = []

    for item in root_path.rglob('*'):
        if any(part == '.git' for part in item.parts):
            continue
        if item.name == '.gitignore':
            continue
        if item.is_symlink() and not follow_symlinks:
            continue
        if spec and is_ignored(item, root_path, spec):
            continue
        if item.is_file():
            rel = item.relative_to(root_path)
            collected.append(rel)
    return collected


def build_tree(files: List[Path]) -> Dict:
    tree = {}
    for path in files:
        parts = path.parts
        current = tree
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = None
    return tree
