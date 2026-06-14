import argparse
import sys
from pathlib import Path

from .collector import collect_files, build_tree
from .reader import read_file
from .formatter import render


def _generate_report(
    root_path: Path,
    include_content=True,
    mask_secrets=False,
    follow_gitignore=True,
    follow_symlinks=False,
    fmt="txt",
):
    print("Scanning files...", file=sys.stderr, flush=True)
    files = collect_files(root_path, follow_gitignore=follow_gitignore, follow_symlinks=follow_symlinks)
    tree = build_tree(files)

    files_content = []
    if include_content:
        total = len(files)
        print(f"Reading {total} files...", file=sys.stderr, flush=True)
        for rel_path in files:
            abs_path = root_path / rel_path
            content = read_file(abs_path, mask_secrets=mask_secrets)
            files_content.append((rel_path, content))
        print(f"Done. Read {total} files.", file=sys.stderr, flush=True)
    else:
        files_content = []

    root_name = root_path.name or str(root_path)
    report = render(root_name, tree, files_content, fmt=fmt)
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Pack your codebase into a single file for AI analysis"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--no-content",
        dest="include_content",
        action="store_false",
        help="Do not include file contents (only show tree structure)"
    )
    parser.add_argument(
        "--mask-secrets",
        action="store_true",
        help="Mask sensitive information like passwords, tokens, etc."
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Write output to a file instead of stdout"
    )
    parser.add_argument(
        "--no-gitignore",
        dest="follow_gitignore",
        action="store_false",
        help="Do NOT respect .gitignore rules (include all files)"
    )
    parser.add_argument(
        "--follow-symlinks",
        action="store_true",
        help="Follow symbolic links during scanning (disabled by default)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["txt", "md"],
        default="txt",
        help="Output format: txt (default) or md",
        metavar='FMT'
    )

    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if not root_path.is_dir():
        print(f"Error: '{root_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    try:
        report = _generate_report(
            root_path,
            include_content=args.include_content,
            mask_secrets=args.mask_secrets,
            follow_gitignore=args.follow_gitignore,
            follow_symlinks=args.follow_symlinks,
            fmt=args.format,
        )
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            args.output.write_text(report, encoding='utf-8')
            print(f"Report written to {args.output}")
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)


if __name__ == "__main__":
    main()
