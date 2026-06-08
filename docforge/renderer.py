from .parser import ModuleDoc, ClassDoc, FunctionDoc


def render_function(fn: FunctionDoc, level: int = 3) -> str:
    prefix = "#" * level
    decorators = "".join(f"`@{d}`  \n" for d in fn.decorators)
    doc = f"\n\n{fn.docstring}" if fn.docstring else ""
    return f"{prefix} `def {fn.name}{fn.signature}`\n\n{decorators}{doc}\n"


def render_class(cls: ClassDoc) -> str:
    bases = f"({', '.join(cls.bases)})" if cls.bases else ""
    doc = f"\n{cls.docstring}\n" if cls.docstring else ""
    methods = "\n".join(render_function(m, level=4) for m in cls.methods)
    return f"## `class {cls.name}{bases}`\n{doc}\n{methods}"


def render_module(mod: ModuleDoc) -> str:
    lines = [f"# `{mod.name}`\n"]
    if mod.docstring:
        lines.append(mod.docstring + "\n")
    if mod.functions:
        lines.append("## Functions\n")
        lines.extend(render_function(fn) for fn in mod.functions)
    if mod.classes:
        lines.append("## Classes\n")
        lines.extend(render_class(cls) for cls in mod.classes)
    return "\n".join(lines)
