from dataclasses import dataclass

import camelsnake
from jinja2 import Environment, PackageLoader, select_autoescape


@dataclass
class Jinja:
    env: Environment


def create_jinja() -> Jinja:
    env = Environment(
        loader=PackageLoader(
            "fastscaffold.resource",
            "std"
        ),
        autoescape=select_autoescape()
    )
    env.filters["camel_to_snake"] = camelsnake.camel_to_snake
    env.filters["snake_to_camel"] = camelsnake.snake_to_camel
    env.filters["no_id"] = lambda data: {
        key: value for key, value in data.items()
        if key != "id"
    } if isinstance(data, dict) else [
        (key, value) for key, value in data
        if key != "id"
    ]
    env.filters["camel_to_human"] = lambda text: (
        camelsnake.camel_to_snake(text).replace("_", " ")
    )
    return Jinja(env)
