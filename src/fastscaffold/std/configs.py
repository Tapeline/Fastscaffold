from dataclasses import dataclass


@dataclass
class WebProjectConfig:
    name: str
    slug: str
    src: str = "src"
