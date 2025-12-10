import textwrap
import importlib

import docstring_parser


def define_env(env):
    @env.macro
    def doc_component(name: str):
        module_name, simple_name = name.rsplit('.', maxsplit=1)
        component_mod = importlib.import_module(module_name)
        component_cls = getattr(component_mod, simple_name)
        docstring = str(getattr(component_cls, "__doc__", ""))
        docstring = docstring_parser.parse(docstring)

        reqs, desc = extract_requirements(
            docstring.description or "No description provided."
        )

        lines = [
            f"## `{simple_name}`",
            "",
            desc,
            "",
        ]

        reqs = [f"- `{requirement}`" for requirement in reqs]

        lines.extend([
            "### Requires",
            "",
            *(reqs if reqs else ["No requirements."]),
            "",
            "### Requires context",
            "",
        ])

        for context_req in component_cls.requires_context:
            lines.append(f"- `{context_req.__qualname__}`")

        lines.extend([
            "### Parameters",
            "",
        ])

        for param in docstring.params:
            lines.extend([
                f"- `{param.arg_name}`: " +
                f"`{component_cls.__init__.__annotations__.get(
                    param.arg_name
                )!r}`",
                "    ",
                f"    {"_Optional_" if param.is_optional else "_Required_"} " +
                f"{f"_Default:_ `{param.default}`" if param.default else ""}",
                "    ",
                textwrap.indent(
                    param.description or "No description provided.",
                    prefix="    ",
                ),
                "",
            ])
        if not docstring.params:
            lines.extend([
                "No parameters.",
                "",
            ])

        for example in docstring.examples:
            lines.extend([
                "!!! example",
                textwrap.indent(
                    example.description or "No description provided.",
                    prefix="    ",
                ),
                "    ",
                textwrap.indent(
                    f"```python\n{example.snippet}\n```",
                    prefix="    ",
                ) if example.snippet else "",
                "",
            ])

        return "\n".join(lines)


def extract_requirements(desc):
    desc = textwrap.dedent(desc).strip()
    requirements = []
    description = []
    in_req = False
    for line in desc.splitlines():
        if line == "Requires:":
            in_req = True
            continue
        if in_req and line.strip():
            requirements.append(line.strip())
        if not line.startswith(" "):
            in_req = False
        if not in_req:
            description.append(line)
    return requirements, "\n".join(description)
