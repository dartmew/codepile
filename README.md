# PilePack

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pilepack)](https://pypi.org/project/pilepack/)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-84%25-yellowgreen)](#-testing)
[![CLI](https://img.shields.io/badge/CLI-ready-blue)](#-usage)

**Pack your codebase into a single file for AI analysis**  
Combine all your project files into one text file — perfect for sending to LLMs (ChatGPT, Claude, Copilot, Deepseek, etc.).

---

## ✨ Features

- 📁 **Recursive scanning** – walks through all files in a directory.
- 🚫 **Respects .gitignore** – optionally disable with `--no-gitignore`.
- 🌳 **Tree structure** – displays project hierarchy.
- 📄 **Embedded content** – each file is shown with its path header.
- 🔐 **Secrets masking** – hides passwords, tokens, keys (`--mask-secrets`).
- 🖨️ **Two output formats** – plain text (`txt`) or Markdown (`md`).
- 💾 **Save to file** – use `-o output.txt`.

---

## 📦 Installation

```bash
pip install pilepack
```
From source:

```bash
git clone https://github.com/dartmew/pilepack.git
cd pilepack
pip install -e .
```

## 🚀 Usage
Basic command – pass a path to your project:
```bash
pilepack /path/to/your/project
```
Redirect output to a file:
```bash
pilepack . > report.txt
```
Example output (txt)
```text
myproject
├── main.py
├── utils/
│   ├── helpers.py
│   └── __init__.py
└── README.md

================================================================================

--- FILE: main.py ---
import utils.helpers

def main():
    print("Hello")

--- FILE: utils/helpers.py ---
def greet(name):
    return f"Hi {name}"
```
Markdown format
```bash
pilepack . -f md -o report.md
```
Produces a Markdown file with syntax highlighting.

Show only structure (no file contents)
```bash
pilepack . --no-content
```
Mask secrets
```bash
pilepack . --mask-secrets
```
Replaces values of password=, api_key=, token=, and long strings (base64/hex) with ***.

Disable .gitignore
```bash
pilepack . --no-gitignore
```
## 📋 CLI Options
| Option | Description |
|--------|-------------|
| `root` | Directory to scan (default: current directory) |
| `--no-content` | Show tree structure only, skip file contents |
| `--mask-secrets` | Mask passwords, tokens, API keys |
| `-o, --output` | Write report to a file instead of stdout |
| `--no-gitignore` | Do not respect `.gitignore` (include all files) |
| `-f, --format` | Output format: `txt` (default) or `md` |

## 🧪 Testing
Install test dependencies and run:

```bash
pip install -e .[test]
pytest
```
With coverage:
```bash
pytest --cov=pilepack
```
Current coverage: 84% (20 tests, all passing).
```bash
Name                    Stmts   Miss  Cover
-------------------------------------------
pilepack\__init__.py        0      0   100%
pilepack\__main__.py        3      3     0%
pilepack\cli.py            51      7    86%
pilepack\collector.py      30      1    97%
pilepack\formatter.py      44      3    93%
pilepack\ignorer.py        21      3    86%
pilepack\reader.py         31     12    61%
-------------------------------------------
TOTAL                     180     29    84%
```

## 📄 License
[MIT](LICENSE) © 2026 Vasili S. Pribylov

## 🤝 Contributing
Issues and pull requests are welcome! For major changes, please open an issue first to discuss.

## 💬 Support

Feel free to [open an issue](https://github.com/dartmew/pilepack/issues) for bugs, questions, or suggestions. I'll try to respond within a few days.

This project is actively maintained (as of 2026).

## 🙏 Acknowledgements
Inspired by the need to easily feed code into large language models.