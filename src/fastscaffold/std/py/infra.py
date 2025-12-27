from fastscaffold.std.gen import (
    SimpleManyTemplatesRender
)


class DockerGen(SimpleManyTemplatesRender):
    location = ["..", "..", "pyproject.toml"]
    templates = {
        "Dockerfile": "infra/Dockerfile.template",
        "docker-compose.yml": "infra/docker-compose.yml.template",
        "start.sh": "infra/start.sh.template",
    }
