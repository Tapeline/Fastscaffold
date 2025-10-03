import textwrap
from pathlib import Path
import yaml


def define_env(env):
    @env.macro
    def doc_component(name):
        component_cls = __import__(name)
        *_, simple_name = name.split('.')
        component = yaml.safe_load(spec)
        lines = [
            f"## `{simple_name}`",
            "",
            getattr(component_cls, "__doc__", "No description provided."),
            "",
            f'???+ example "Подключить к CI"',
            f"    ``` yaml",
            f"    include:",
            f"      - component: git.bytes2b.ru/er-gpt/ci-components/{name}@master",
            f"    ```",
            "",
            f"## Входы"
        ]
        for input_name, input_data in component["spec"]["inputs"].items():
            input_default = input_data.get('default', 'нет значения по умолчанию')
            input_desc = input_data.get('description', '')
            lines.extend((
                f"### `{input_name}`",
                f"> По умолчанию: `{input_default}`",
                "",
                f"{input_desc}",
                ""
            ))
        return "\n".join(lines)
