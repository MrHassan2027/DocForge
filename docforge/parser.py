import ast
import inspect
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FunctionDoc:
    name: str
    signature: str
    docstring: str
    decorators: list[str]


@dataclass
class ClassDoc:
    name: str
    docstring: str
    bases: list[str]
    methods: list[FunctionDoc] = field(default_factory=list)


@dataclass
class ModuleDoc:
    name: str
    docstring: str
    functions: list[FunctionDoc] = field(default_factory=list)
    classes: list[ClassDoc] = field(default_factory=list)


def _get_annotation(node: ast.expr | None) -> str:
    if node is None:
        return ""
    return ast.unparse(node)


def _parse_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionDoc:
    args = []
    for arg in node.args.args:
        ann = f": {_get_annotation(arg.annotation)}" if arg.annotation else ""
        args.append(f"{arg.name}{ann}")
    returns = f" -> {_get_annotation(node.returns)}" if node.returns else ""
    sig = f"({', '.join(args)}){returns}"
    decorators = [ast.unparse(d) for d in node.decorator_list]
    docstring = ast.get_docstring(node) or ""
    return FunctionDoc(name=node.name, signature=sig, docstring=docstring, decorators=decorators)


def parse_file(path: Path) -> ModuleDoc:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    module_doc = ast.get_docstring(tree) or ""
    functions: list[FunctionDoc] = []
    classes: list[ClassDoc] = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_parse_function(node))
        elif isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases]
            class_doc = ast.get_docstring(node) or ""
            methods = [
                _parse_function(m)
                for m in ast.iter_child_nodes(node)
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            classes.append(ClassDoc(name=node.name, docstring=class_doc, bases=bases, methods=methods))

    return ModuleDoc(name=path.stem, docstring=module_doc, functions=functions, classes=classes)
