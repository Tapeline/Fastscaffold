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
    InteractorDIProviderGen, LitestarAppGen,
    LitestarAuthProviderGen,
    LitestarStructlogLoggingGen,
    TransactionManagerProviderGen,
)
from fastscaffold.std.py.common import DataCommonsGen
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
        ctx += WebProjectConfig("Example backend", "example_backend")
        ctx += create_jinja()

        return [
            DataCommonsGen(),
            EntityGen(
                name="User",
                fields=dict(
                    username="str",
                ),
                with_id=True
            ),
            EntityGen(
                name="SomeEntity",
                fields=dict(
                    name="str",
                    field_a="str",
                    field_b="str",
                ),
                with_id=True,
            ),
            EntityGen(
                name="SomeUserEntity",
                fields=dict(
                    name="str",
                    field_a="str",
                    author_id="UserId"
                ),
                with_id=True,
                add_imports=[
                    "from example_backend.domain.user import UserId"
                ],
            ),
            TransactionManagerInterfaceGen(),
            PaginationDTOGen(),
            UUIDGeneratorInterfaceGen(),
            GatewayInterfaceGen(
                "User",
                GatewayInterfaceGen.add_get_by_id(),
                GatewayInterfaceGen.add_save()
            ),
            GatewayInterfaceGen(
                "SomeEntity",
                GatewayInterfaceGen.add_get_by_id(),
                GatewayInterfaceGen.add_save(),
                GatewayInterfaceGen.add_get_paginated_filtered("list_all"),
                GatewayInterfaceGen.add_delete_by_id(),
                gen_exceptions=True
            ),
            GatewayInterfaceGen(
                "SomeUserEntity",
                GatewayInterfaceGen.add_get_by_id(),
                GatewayInterfaceGen.add_save(),
                GatewayInterfaceGen.add_get_paginated_filtered(
                    "get_of_user",
                    author_id="UserId"
                ),
                GatewayInterfaceGen.add_delete_by_id(),
                gen_exceptions=True
            ),
            BasicAppAuthGen("User"),
            BasicAppAuthInteractorsGen("User"),
            CreateInteractorGen("SomeEntity"),
            ReadInteractorGen("SomeEntity", with_auth=False),
            UpdateInteractorGen("SomeEntity"),
            DeleteInteractorGen("SomeEntity"),
            ListInteractorGen(
                "SomeEntity",
                gw_list_method="list_all",
                name="ListAllSomeEntities",
                with_auth=False
            ),
            CreateInteractorGen("SomeUserEntity"),
            ReadInteractorGen("SomeUserEntity"),
            UpdateInteractorGen("SomeUserEntity"),
            DeleteInteractorGen("SomeUserEntity"),
            ListInteractorGen(
                "SomeUserEntity",
                gw_list_method="get_of_user"
            ),
            AlembicGen(),
            SqlalchemyTransactionManagerGen(),
            SqlalchemyModelsGen(["User", "SomeUserEntity", "SomeEntity"]),
            SqlalchemySimpleGatewayImplGen(
                "User",
                get_by_id=True, save=True
            ),
            AddImports(
                src_in("infrastructure", "persistence", "user.py"),
                "from example_backend.application.auth.exceptions import UserNotFound"
            ),
            SqlalchemySimpleGatewayImplGen(
                "SomeEntity",
                get_by_id=True, save=True
            ),
            SqlalchemySimpleGatewayImplGen(
                "SomeUserEntity",
                get_by_id=True, save=True
            ),
            SqlalchemySecurityGen(),
            UUIDGeneratorImplGen(),
            ArgonSecurityGen(),
            LitestarCommonsGen(),
            LitestarCommonUserEndpointsGen(),
            SqlalchemySessionGen(),
            ConfigGen(
                DEFAULT_PG_CONF,
                DEFAULT_SECURITY_CONF,
                DEFAULT_LOGGING_CONF,
            ),
            ConfigDIProviderGen(),
            AlgoDIProviderGen(),
            InteractorDIProviderGen(),
            LitestarAuthProviderGen(),
            TransactionManagerProviderGen(),
            FuenteConfigLoaderGen(),
            LitestarStructlogLoggingGen(),
            LitestarAppGen(add_prometheus=True),
            PyprojectGen(),
            PyQAConfigsGen(),
            SuperSimpleTestsTemplateGen(),
            JustfileGen(),
        ]

    executor = ScaffoldExecutor()
    files = executor.run(scaffold)
    save_files("example_backend", files)


if __name__ == "__main__":
    test()
