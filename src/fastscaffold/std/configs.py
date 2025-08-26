from dataclasses import dataclass


@dataclass
class WebProjectConfig:
    name: str
    slug: str
    src: str = "src"


@dataclass
class ArchitectureConfig:
    application_pkg: str = "application"
    infrastructure_pkg: str = "infrastructure"
    bootstrap_pkg: str = "bootstrap"
    domain_pkg: str = "domain"
    presentation_pkg: str = "presentation"
