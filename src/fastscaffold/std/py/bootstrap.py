from dataclasses import dataclass, field
from typing import Any

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.files import ScaffoldFile
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import SimpleTemplateRender, src_in
from fastscaffold.std.py.infrastructure.persistence import TransactionManagerWasGenerated


@dataclass
class GeneratedDIProvider:
    import_line: str
    name: str


@dataclass
class DIProviderStore:
    providers: list[GeneratedDIProvider]


def _get_or_create_di_provider_store(
    ctx: ScaffoldRunContext
) -> DIProviderStore:
    if DIProviderStore not in ctx:
        ctx += DIProviderStore([])
    return ctx[DIProviderStore]


@dataclass
class GeneratedConfig:
    simple_name: str
    fields: dict[str, str]
    defaults: dict[str, str] = field(default_factory=dict)
    name: str = ""

    def __post_init__(self):
        self.name = f"{self.simple_name}Config"


DEFAULT_PG_CONF = GeneratedConfig(
    "Postgres",
    fields=dict(
        host="str",
        port="int",
        username="str",
        password="str",
        database="str",
    )
)
DEFAULT_SECURITY_CONF = GeneratedConfig(
    "Security",
    fields=dict(
        session_lifetime="timedelta",
    ),
    defaults=dict(
        session_lifetime="timedelta(hours=48)"
    )
)
DEFAULT_LOGGING_CONF = GeneratedConfig(
    "Logging",
    fields=dict(
        use_json="bool",
    ),
    defaults=dict(
        use_json="False"
    )
)


@dataclass
class ConfigStore:
    configs: list[GeneratedConfig]

    @property
    def name_mapped(self) -> dict[str, GeneratedConfig]:
        return {
            config.simple_name: config
            for config in self.configs
        }


class LitestarAppGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        DIProviderStore
    ]
    location = ["bootstrap", "app.py"]
    template = "bootstrap/litestar_app.py.template"

    def __init__(self, *, add_prometheus: bool = False) -> None:
        super().__init__()
        self.add_prometheus = add_prometheus

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            di_providers=ctx[DIProviderStore].providers,
        )


class ConfigDIProviderGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        ConfigStore
    ]
    location = ["bootstrap", "di", "config.py"]
    template = "bootstrap/config_di_provider.py.template"

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            configs=ctx[ConfigStore].configs
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        slug = ctx[WebProjectConfig].slug
        _get_or_create_di_provider_store(ctx).providers.append(
            GeneratedDIProvider(
                import_line=(
                    f"from {slug}.bootstrap.di.config "
                    f"import ConfigDIProvider"
                ),
                name="ConfigDIProvider"
            )
        )


class ConfigGen(SimpleTemplateRender):
    location = ["config.py"]
    template = "bootstrap/config.py.template"

    def __init__(self, *configs: GeneratedConfig) -> None:
        self.configs = list(configs)

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            configs=self.configs
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        ctx += ConfigStore(configs=self.configs)


class LitestarAuthProviderGen(SimpleTemplateRender):
    location = ["bootstrap", "di", "auth.py"]
    template = "bootstrap/litestar_auth_provider.py.template"

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        slug = ctx[WebProjectConfig].slug
        _get_or_create_di_provider_store(ctx).providers.append(
            GeneratedDIProvider(
                import_line=(
                    f"from {slug}.bootstrap.di.auth "
                    f"import AuthSessionDIProvider"
                ),
                name="AuthSessionDIProvider"
            )
        )


class TransactionManagerProviderGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        TransactionManagerWasGenerated,
    ]
    location = ["bootstrap", "di", "transactions.py"]
    template = "bootstrap/transactions_di_provider.py.template"

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        slug = ctx[WebProjectConfig].slug
        _get_or_create_di_provider_store(ctx).providers.append(
            GeneratedDIProvider(
                import_line=(
                    f"from {slug}.bootstrap.di.transactions "
                    f"import TransactionManagerDIProvider"
                ),
                name="TransactionManagerDIProvider"
            )
        )


class AlgoDIProviderGen(SimpleTemplateRender):
    location = ["bootstrap", "di", "algorithms.py"]
    template = "bootstrap/algo_di_provider.py.template"

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        slug = ctx[WebProjectConfig].slug
        _get_or_create_di_provider_store(ctx).providers.append(
            GeneratedDIProvider(
                import_line=(
                    f"from {slug}.bootstrap.di.algorithms "
                    f"import AlgorithmsDIProvider"
                ),
                name="AlgorithmsDIProvider"
            )
        )


class InteractorDIProviderGen(SimpleTemplateRender):
    location = ["bootstrap", "di", "interactors.py"]
    template = "bootstrap/interactors_di_provider.py.template"

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        slug = ctx[WebProjectConfig].slug
        _get_or_create_di_provider_store(ctx).providers.append(
            GeneratedDIProvider(
                import_line=(
                    f"from {slug}.bootstrap.di.interactors "
                    f"import InteractorsDIProvider"
                ),
                name="InteractorsDIProvider"
            )
        )


class FuenteConfigLoaderGen(SimpleTemplateRender):
    location = ["bootstrap", "config.py"]
    template = "bootstrap/fuente_config_loader.py.template"

    def build(self, ctx: ScaffoldRunContext) -> None:
        super().build(ctx)
        cfg_filename = f"{ctx[WebProjectConfig].slug}.yml"
        ctx.files[cfg_filename] = ScaffoldFile(
            cfg_filename,
            ["# TODO: fill config"],
            ctx
        )


class LitestarStructlogLoggingGen(SimpleTemplateRender):
    location = ["bootstrap", "logging.py"]
    template = "bootstrap/litestar_structlog_logging.py.template"
