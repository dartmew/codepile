import argparse
import sys
from pathlib import Path
from typing import TextIO
from .collector import collect_files, build_tree
from .reader import read_file
from .formatter import write_report
from . import __version__


def _stream_report(
    root_path: Path,
    stream: TextIO,
    include_content: bool = True,
    mask_secrets: bool = False,
    follow_gitignore: bool = True,
    follow_symlinks: bool = False,
    fmt: str = 'txt',
) -> None:
    '''Generate report and write directly to stream (no memory accumulation).'''
    print("Scanning files...", file=sys.stderr, flush=True)
    files = collect_files(root_path, follow_gitignore=follow_gitignore, follow_symlinks=follow_symlinks)
    tree = build_tree(files)

    root_name = root_path.name or str(root_path)

    if not include_content:
        # Empty generator – no file contents
        def empty_gen():
            return iter([])
        write_report(stream, root_name, tree, empty_gen(), fmt=fmt)
        return

    total = len(files)
    print(f'Reading {total} files...', file=sys.stderr, flush=True)

    def content_generator():
        for i, rel_path in enumerate(files, 1):
            abs_path = root_path / rel_path
            content = read_file(abs_path, mask_secrets=mask_secrets)
            yield rel_path, content
            if i % 100 == 0:
                print(f'Processed {i}/{total} files...', file=sys.stderr, flush=True)
        print(f'Done. Read {total} files.', file=sys.stderr, flush=True)

    write_report(stream, root_name, tree, content_generator(), fmt=fmt)


def main():
    parser = argparse.ArgumentParser(
        description='Pack your codebase into a single file for AI analysis'
    )
    parser.add_argument(
        'root',
        nargs='?',
        default='.',
        help='Root directory to scan (default: current directory)',
    )
    parser.add_argument(
        '--no-content',
        dest='include_content',
        action='store_false',
        help='Do not include file contents (only show tree structure)'
    )
    parser.add_argument(
        '--mask-secrets',
        action='store_true',
        help='Mask sensitive information like passwords, tokens, etc.'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Write output to a file instead of stdout'
    )
    parser.add_argument(
        '--no-gitignore',
        dest='follow_gitignore',
        action='store_false',
        help='Do NOT respect .gitignore rules (include all files)'
    )
    parser.add_argument(
        '--follow-symlinks',
        action='store_true',
        help='Follow symbolic links during scanning (disabled by default)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md'],
        default='txt',
        help='Output format: txt (default) or md',
        metavar='FMT'
    )
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version=f'pilepack {__version__}'
    )

    args = parser.parse_args()

    root_path = Path(args.root).resolve()

    if not root_path.is_dir():
        print(f"Error: '{root_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                _stream_report(
                    root_path,
                    f,
                    include_content=args.include_content,
                    mask_secrets=args.mask_secrets,
                    follow_gitignore=args.follow_gitignore,
                    follow_symlinks=args.follow_symlinks,
                    fmt=args.format,
                )
            print(f'Report written to {args.output}')
        else:
            _stream_report(
                root_path,
                sys.stdout,
                include_content=args.include_content,
                mask_secrets=args.mask_secrets,
                follow_gitignore=args.follow_gitignore,
                follow_symlinks=args.follow_symlinks,
                fmt=args.format,
            )
    except Exception as e:
        print(f'Error generating report: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
