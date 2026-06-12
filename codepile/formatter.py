from typing import Dict


def format_tree(tree: Dict, prefix: str = '', is_last: bool = True) -> str:
    lines = []
    items = sorted(tree.items(), key=lambda x: (isinstance(x[1], dict), x[0].lower()), reverse=True)
    for i, (name, subtree) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        connector = '└── ' if is_last_item else '├── '
        display_name = name + '/' if isinstance(subtree, dict) else name
        lines.append(prefix + connector + display_name)
        if isinstance(subtree, dict):
            new_prefix = prefix + ('    ' if is_last_item else '│   ')
            lines.append(format_tree(subtree, new_prefix, is_last_item))
    return '\n'.join(lines)
