# DocForge

> Parse Python source into structured Markdown docs — like pdoc, but zero dependencies

## What it does
Reads Python source files using the `ast` module, extracts docstrings, function signatures, type annotations, and class hierarchies, then generates clean Markdown documentation. No imports of the target module — purely static AST analysis.

## Quick Start
```bash
git clone https://github.com/MrHassan2027/DocForge
cd DocForge
pip install -e .
docforge ./mypackage -o ./docs
```

```
docs/
├── index.md
├── mypackage.module1.md
└── mypackage.module2.md
```

## Features
- Zero dependencies — only `ast` from stdlib
- Extracts: module docstring, classes, methods, functions, type annotations
- Generates index page with cross-links
- `--format` flag: `markdown` (default) or `html`
- Handles `@property`, `@classmethod`, `@staticmethod` decorators
- `--private` flag to include `_underscore` members

## Tech Stack
| Tool | Why |
|------|-----|
| Python 3.11+ | `ast.parse()` for static analysis |
| No deps | Single-file install, works offline |

## Example Output
```markdown
## `class UserService`

Manages user accounts and authentication.

### `def create_user(name: str, email: str) -> User`

Creates a new user and persists to database.

**Args:**
- `name` (str): Display name
- `email` (str): Must be unique

**Returns:** `User` — the created user instance
```
