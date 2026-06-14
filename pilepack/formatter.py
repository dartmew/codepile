from typing import Dict, TextIO


def _format_tree(tree: Dict, prefix: str = '', is_last: bool = True) -> str:
    lines = []
    items = sorted(tree.items(), key=lambda x: (isinstance(x[1], dict), x[0].lower()), reverse=True)

    for i, (name, subtree) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        connector = '└── ' if is_last_item else '├── '
        display_name = name + '/' if isinstance(subtree, dict) else name
        lines.append(prefix + connector + display_name)

        if isinstance(subtree, dict):
            new_prefix = prefix + ('    ' if is_last_item else '│   ')
            lines.append(_format_tree(subtree, new_prefix, is_last_item))
    return '\n'.join(lines)


def _write_txt(
    stream: TextIO,
    root_name: str,
    tree: Dict,
    files_content_gen,  # generator of (Path, Optional[str])
) -> None:

    stream.write(f"{root_name}\n")
    stream.write(_format_tree(tree))
    stream.write("\n\n")
    stream.write("=" * 80)
    stream.write("\n\n")

    for rel_path, content in files_content_gen:
        if content is not None:
            stream.write(f"--- FILE: {rel_path} ---\n")
            stream.write(content)
            stream.write("\n\n")
        else:
            stream.write(f"--- FILE: {rel_path} [BINARY OR UNREADABLE] ---\n\n")


def _write_md(
    stream: TextIO,
    root_name: str,
    tree: Dict,
    files_content_gen,
) -> None:
    stream.write(f"# {root_name}\n\n```\n{_format_tree(tree)}\n```\n\n---\n\n")

    for rel_path, content in files_content_gen:
        if content is not None:
            ext = rel_path.suffix.lower()
            lang = {
                '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                '.html': 'html', '.css': 'css', '.json': 'json',
                '.md': 'markdown', '.yaml': 'yaml', '.yml': 'yaml',
                '.sh': 'bash', '.txt': 'text'
            }.get(ext, 'text')
            stream.write(f"## `{rel_path}`\n\n```{lang}\n{content}\n```\n\n")
        else:
            stream.write(f"## `{rel_path}`\n\n*[BINARY OR UNREADABLE]*\n\n")


def write_report(
    stream: TextIO,
    root_name: str,
    tree: Dict,
    files_content_gen,
    fmt: str = "txt",
) -> None:
    if fmt == "txt":
        _write_txt(stream, root_name, tree, files_content_gen)
    elif fmt == "md":
        _write_md(stream, root_name, tree, files_content_gen)
    else:
        raise ValueError(f"Unsupported format: {fmt}. Supported: 'txt', 'md'")