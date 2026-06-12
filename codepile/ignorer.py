from pathlib import Path
from pathspec import PathSpec


def load_gitignore(root_path: Path) -> PathSpec:
    gitignore_path = root_path / '.gitignore'
    if not gitignore_path.exists():
        return PathSpec.from_lines('gitignore', [])
    with open(gitignore_path, 'r', encoding='utf-8') as file:
        return PathSpec.from_lines('gitignore', file)


def is_ignored(path, root: Path, spec: PathSpec) -> bool:
    original = str(path)
    path_obj = Path(original)

    if not path_obj.is_absolute():
        path_obj = root / path_obj

    try:
        rel_path = path_obj.relative_to(root)
    except ValueError:
        return False
    rel_str = rel_path.as_posix()

    if original.endswith(('/', '\\')) or (path_obj.exists() and path_obj.is_dir()):
        rel_str += '/'
    return spec.match_file(rel_str)
