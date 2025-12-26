from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.execution import ScaffoldExecutor
from fastscaffold.io import save_files
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import AddImports, SourceGen, import_from, src_in
from fastscaffold.std.jinja import create_jinja
from fastscaffold.std.py.algo import ArgonSecurityGen
from fastscaffold.std.py.application.basic_user import (
    BasicAppAuthGen,
    BasicAppAuthInteractorsGen,
)
from fastscaffold.std.py.application.interactors import (
    CreateInteractorGen,
    DeleteInteractorGen,
    ListInteractorGen,
    ReadInteractorGen,
    UpdateInteractorGen,
)
from fastscaffold.std.py.application.persistence import (
    PaginationDTOGen,
    TransactionManagerInterfaceGen, UUIDGeneratorInterfaceGen,
)
from fastscaffold.std.py.application.persistence import GatewayInterfaceGen
from fastscaffold.std.py.bootstrap import (
    AlgoDIProviderGen,
    ConfigDIProviderGen,
    ConfigGen,
    DEFAULT_LOGGING_CONF, DEFAULT_PG_CONF,
    DEFAULT_SECURITY_CONF,
    FuenteConfigLoaderGen,
    LitestarAppGen,
    LitestarAuthProviderGen,
    LitestarStructlogLoggingGen,
    TransactionManagerProviderGen,
)
from fastscaffold.std.py.configs import (
    JustfileGen,
    PyQAConfigsGen,
    PyprojectGen,
)
from fastscaffold.std.py.domain import EntityGen
from fastscaffold.std.py.infrastructure.persistence import (
    AlembicGen,
    SqlalchemyModelsGen,
    SqlalchemySecurityGen, SqlalchemySessionGen,
    SqlalchemySimpleGatewayImplGen,
    SqlalchemyTransactionManagerGen, UUIDGeneratorImplGen,
)
from fastscaffold.std.py.presentation.litestar import (
    LitestarCommonUserEndpointsGen,
    LitestarCommonsGen,
)
from fastscaffold.std.py.tests import SuperSimpleTestsTemplateGen


def test():
    def scaffold(ctx: ScaffoldRunContext) -> list[ScaffoldComponent]:
        ctx += WebProjectConfig("Midlegram server", "midlegram")
        ctx += create_jinja()

        return [
            LitestarCommonsGen(),
            ConfigGen(
                DEFAULT_LOGGING_CONF,
            ),
            ConfigDIProviderGen(),
            FuenteConfigLoaderGen(),
            LitestarStructlogLoggingGen(),
            LitestarAppGen(add_prometheus=True),
            PyprojectGen(),
            PyQAConfigsGen(),
            JustfileGen(),
        ]

    executor = ScaffoldExecutor()
    files = executor.run(scaffold)
    #save_files("../../GeneratedNoteTakingApp", files)
    save_files("midlegram", files)


if __name__ == "__main__":
    test()
